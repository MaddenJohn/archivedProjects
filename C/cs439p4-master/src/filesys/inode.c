#include "filesys/inode.h"
#include <list.h>
#include <debug.h>
#include <round.h>
#include <string.h>
#include "filesys/filesys.h"
#include "filesys/free-map.h"
#include "threads/malloc.h"
#include "threads/palloc.h"
#include "threads/synch.h"
#include "filesys/directory.h"
#include "threads/thread.h"

/* Identifies an inode. */
#define INODE_MAGIC 0x494e4f44
#define NUM_DIRECT_BLOCKS 121
#define INVALID_SECTOR 16500
#define BLOCK_POINTERS 128
#define PGSIZE 4096

/* Functions for Project 4. */
static void free_ind_block (block_sector_t *indirect);
static void free_doub_block (block_sector_t *double_indirect);
static int allocate_doub_block (block_sector_t *double_indirect, 
                                block_sector_t sectors, int start);
static int allocate_ind_block (block_sector_t *indirect, 
                               block_sector_t sectors, int start);
static block_sector_t find_doubly_indirect (block_sector_t doub_indirect,
                                            block_sector_t offset);
static block_sector_t find_indirect (block_sector_t indirect_block, 
                                     block_sector_t offset);

/* On-disk inode.
   Must be exactly BLOCK_SECTOR_SIZE bytes long. */
struct inode_disk
  {
    block_sector_t direct_blocks[NUM_DIRECT_BLOCKS]; /* 123 direct blocks. */
    block_sector_t indirect_block;     /* 1 first-level indirection block. */
    block_sector_t double_indirect;    /* 1 second-level indirection block. */
    off_t length;                      /* File size in bytes.*/ 
    int is_direct;
    unsigned magic;                    /* Magic number. */
    block_sector_t parent;
    int num_children;
  };

/* Returns the number of sectors to allocate for an inode SIZE
   bytes long. */
static inline size_t
bytes_to_sectors (off_t size)
{
  return DIV_ROUND_UP (size, BLOCK_SECTOR_SIZE);
}

/* In-memory inode. */
struct inode 
  {
    struct list_elem elem;              /* Element in inode list. */
    block_sector_t sector;              /* Sector number of disk location. */
    int open_cnt;                       /* Number of openers. */
    bool removed;                       /* True if deleted, false otherwise. */
    int deny_write_cnt;                 /* 0: writes ok, >0: deny writes. */
    struct inode_disk data;             /* Inode content. */
    struct lock extend_lock;            /* Lock for extending files. */
    struct lock read_write_lock;        /* Readers writers lock. */
    int readers;                        /* Number of current readers. */
    int writers;                        /* Number of current writers. */
    struct condition readers_cv;        /* Condition variable for readers. */
    struct condition writers_cv;        /* Condition variable for writers. */
  };

/* Returns count of openers in the inode. */
int
inode_open_count (struct inode *inode)
{
  /* Matthew driving */
  return inode->open_cnt;
}

/* Takes in a path name and returns the last directory in the name 
   returns null if no such directory exists, caller must close the 
   returned struct dir. */
struct dir*
get_last_dir (const char *path)
{
  /* Matthew, John, and Kirsten driving */
  char *name_copy;
  char *save_ptr = NULL; 
  char *token = NULL;
  const char *fake_path = path;
  char *copy = (char *)palloc_get_page (0);
  if (copy == NULL)
      PANIC ("palloc_get_page(0) return NULL");
  strlcpy (copy, path, PGSIZE);
  name_copy = (char *)palloc_get_page (0);
  if (name_copy == NULL)
    PANIC ("palloc_get_page(0) return NULL");
  strlcpy (name_copy, path, PGSIZE);
  struct dir *dir = NULL;
  struct inode *inode = NULL;
  char *first_occur = NULL;

  /* Remove last "token" from path */
  size_t path_length = strlen (path);
  first_occur = strchr (fake_path, '/');
  if (first_occur == NULL)
    {
      dir = dir_open (inode_open (thread_current ()->dir_inode));
      goto done;
    }
  else if (strcmp (first_occur, "/") == 0)
    {
      dir = dir_open_root ();
      goto done;
    }
      
  fake_path = strrchr (first_occur, '/');
  if (path_length == strlen (first_occur) 
      && strcmp (first_occur, fake_path) == 0)
    {
      dir = dir_open_root ();
      goto done;
    }

  int f_len = strlen (fake_path);
  int new_len = path_length - f_len + 1;
  strlcpy (copy, path, new_len);
  if (*copy == '/')
    dir = dir_open_root ();
  else
    dir = dir_open (inode_open (thread_current ()->dir_inode));

  token = strtok_r (copy, "/", &save_ptr);
  struct dir *old_dir = NULL; 
  if (token != NULL)
    {
      do 
      {
        old_dir = dir;
        // if (strcmp (token, ".")) 
        //   dir = dir;
        // else if (strcmp (token, ".."))
        //   dir = dir_open (inode_open (thread_current ()->parent->dir_inode));
        if (!dir_lookup (dir, token, &inode))
          {
            dir = NULL;
            dir_close (old_dir);
            break;
          }
        else
          {
            dir = dir_open (inode);
            dir_close (old_dir);
          }
      }
      while ((token = strtok_r (NULL, "/", &save_ptr)) != NULL);
    }
  done:
    palloc_free_page (copy);
    palloc_free_page (name_copy);
    return dir;
}

void
inode_set_parent (block_sector_t par, struct inode *ch)
{
  ch->data.parent = par;
}

block_sector_t
inode_get_parent (struct inode *inode)
{
  return inode->data.parent;
}

void
inode_chld_increment (struct inode* inode)
{
  inode->data.num_children++;
}

void
inode_chld_decrement (struct inode* inode)
{
  inode->data.num_children--;
}

bool
inode_has_entries (struct inode* inode)
{
  if (inode->data.num_children > 0)
    return true;
  return false;
}

int
inode_num_entries (struct inode* inode)
{
  return inode->data.num_children;
}

/* Finds the sector of the indirect block. */
static block_sector_t
find_indirect (block_sector_t indirect_block, block_sector_t offset)
{
  /* Matthew and John driving */
  block_sector_t sector = INVALID_SECTOR;
  block_sector_t *buffer = (block_sector_t *)malloc (4 * BLOCK_POINTERS);
  block_read (fs_device, indirect_block, buffer);
  sector = buffer[offset];
  free (buffer);
  return sector;
}

/* Finds the sector of the double indirect block. */
static block_sector_t
find_doubly_indirect (block_sector_t doub_indirect, block_sector_t offset)
{
  /* Matthew and John driving */
  block_sector_t sector = INVALID_SECTOR;
  block_sector_t *doub_buffer = (block_sector_t *)malloc (4 * BLOCK_POINTERS);
  block_read (fs_device, doub_indirect, doub_buffer);
  block_sector_t *ind_buffer = (block_sector_t *)malloc (4 * BLOCK_POINTERS);
  block_read (fs_device, doub_buffer[offset/BLOCK_POINTERS], ind_buffer);
  sector = ind_buffer[offset % BLOCK_POINTERS];
  free (ind_buffer);
  free (doub_buffer);
  return sector;
}

/* Returns the block device sector that contains byte offset POS
   within INODE.
   Returns -1 if INODE does not contain data for a byte at offset
   POS. */
static block_sector_t
byte_to_sector (const struct inode *inode, off_t pos) 
{
  /* Matthew, John, and Kirsten driving */
  ASSERT (inode != NULL);
  int sector = pos/BLOCK_SECTOR_SIZE;
  if (pos < inode->data.length)
    {
      if (sector < NUM_DIRECT_BLOCKS)
        return inode->data.direct_blocks[sector];
      else if (sector < (NUM_DIRECT_BLOCKS + BLOCK_POINTERS))
        return find_indirect (inode->data.indirect_block, 
                              sector - NUM_DIRECT_BLOCKS);
      else if (sector < (BLOCK_POINTERS * BLOCK_POINTERS))
        return find_doubly_indirect (inode->data.double_indirect, sector - 
                                     NUM_DIRECT_BLOCKS - BLOCK_POINTERS);
    }
  return -1;
}

/* List of open inodes, so that opening a single inode twice
   returns the same `struct inode'. */
static struct list open_inodes;

/* Initializes the inode module. */
void
inode_init (void) 
{
  list_init (&open_inodes);
}

/* Allocates sectors data blocks and an indirect block on the disk, initializes
   all data blocks to 0 and returns the number of data block sectors 
   allocated. */
static int  
allocate_ind_block (block_sector_t *indirect, block_sector_t sectors, 
                    int start)
{
  /* Matthew driving */
  block_sector_t indirect_block[BLOCK_POINTERS];
  /* Load in the indirect block if disk space has already been allocated */
  if (*indirect != INVALID_SECTOR)
    block_read (fs_device, *indirect, indirect_block);
  int direct_blocks_allocated = 0;
  static char zeros[BLOCK_SECTOR_SIZE];
  if (sectors > BLOCK_POINTERS)
    sectors = BLOCK_POINTERS;
  unsigned i = start - NUM_DIRECT_BLOCKS; 
  /* Allocate all the data blocks */
  for (; i < sectors; i++)
  {
    if (free_map_allocate (1, &indirect_block[i]))
      {
        direct_blocks_allocated++;
        block_write (fs_device, indirect_block[i], zeros);
      }
    else
      PANIC ("free_map_allocate failed in allocate_ind_block");
      
  }
  /* Write out the indirect block sector */
  if (*indirect == INVALID_SECTOR)
    {
      if (free_map_allocate (1, indirect))
        {
          block_write (fs_device, *indirect, indirect_block);
          return direct_blocks_allocated;
        }
      else
        PANIC ("free_map_allocate failed in allocate_ind_block");
    }
  block_write (fs_device, *indirect, indirect_block);
  return direct_blocks_allocated;
}

/* Allocates sectors data blocks and a doubly indirect block on the disk, 
   initializes all data blocks to 0 and returns the number of data block 
   sectors allocated. */
static int 
allocate_doub_block (block_sector_t *double_indirect, block_sector_t sectors, 
                     int start)
{
  /* Kirsten driving */
  block_sector_t double_indirect_block[BLOCK_POINTERS];
  /* Load in double indirect block if disk space has already been allocated */
  if (*double_indirect != INVALID_SECTOR)
    block_read (fs_device, *double_indirect, double_indirect_block);
  int num_indirect_blocks = (sectors / BLOCK_POINTERS) + 1;
  int sectors_allocated = 0;
  int total_allocated = 0;
  /* Update i to start at next indirect block within double indirect block */
  int i = (start - BLOCK_POINTERS - NUM_DIRECT_BLOCKS) / BLOCK_POINTERS;
  int offset = (start - BLOCK_POINTERS - NUM_DIRECT_BLOCKS) % BLOCK_POINTERS;
  if (num_indirect_blocks > BLOCK_POINTERS)
    num_indirect_blocks = BLOCK_POINTERS;
  bool first = true;
  /* Allocate all the indirect and data blocks */
  for (; i < num_indirect_blocks; i++)
  {
    int num_sec = sectors < BLOCK_POINTERS ? sectors : BLOCK_POINTERS;
    if (first)
      {
        if (num_sec > BLOCK_POINTERS - offset)
          num_sec = BLOCK_POINTERS - offset;
        sectors_allocated = allocate_ind_block (&double_indirect_block[i], 
                                                num_sec, NUM_DIRECT_BLOCKS
                                                + offset);
        first = false;
      }
    else
      sectors_allocated = allocate_ind_block (&double_indirect_block[i], 
                                              num_sec, NUM_DIRECT_BLOCKS);
    sectors -= sectors_allocated;
    total_allocated += sectors_allocated;
  }
  /* Write out the double indirect block sector */
  if (*double_indirect == INVALID_SECTOR)
    {
      if (free_map_allocate (1, double_indirect))
        {
          block_write (fs_device, *double_indirect, double_indirect_block);
          return sectors_allocated;
        }
      else
        PANIC ("free map allocate failed allocating double indirect block");
    }
  block_write (fs_device, *double_indirect, double_indirect_block);
  return sectors_allocated;
}

/* Allocates the correct amount of zeros when extending the file. */
static int 
allocate_zeros (int sectors, struct inode_disk *disk_inode, int next_block)
{
  /* John and Kirsten driving */
  static char zeros[BLOCK_SECTOR_SIZE];
  int allocated = 0;
  int pos = next_block;
  while (sectors > 0)
    { 
      if (next_block < NUM_DIRECT_BLOCKS)
        {  
          if (free_map_allocate (1, &disk_inode->direct_blocks[next_block]))
            {
              block_write (fs_device, 
                           disk_inode->direct_blocks[next_block], zeros); 
              allocated = 1;
            } 
        }
      else if (next_block < (NUM_DIRECT_BLOCKS + BLOCK_POINTERS))
        {
          allocated = allocate_ind_block (&disk_inode->indirect_block,
                                         (sectors + next_block) - 
                                          NUM_DIRECT_BLOCKS, next_block); 
        }
      else if (next_block < (BLOCK_POINTERS * BLOCK_POINTERS))
        {
          allocated = allocate_doub_block (&disk_inode->double_indirect, 
                                          (sectors + next_block) - 
                                           NUM_DIRECT_BLOCKS - BLOCK_POINTERS,
                                           next_block);
        }
        next_block += allocated;
        sectors -= allocated;
    }
  return (next_block - pos);
}

/* Initializes an inode with LENGTH bytes of data and
   writes the new inode to sector SECTOR on the file system
   device.
   Returns true if successful.
   Returns false if memory or disk allocation fails. */
bool
inode_create (block_sector_t sector, off_t length, bool dir)
{
  struct inode_disk *disk_inode = NULL;
  bool success = false;

  ASSERT (length >= 0);

  /* If this assertion fails, the inode structure is not exactly
     one sector in size, and you should fix that. */
  ASSERT (sizeof *disk_inode == BLOCK_SECTOR_SIZE);

  disk_inode = calloc (1, sizeof *disk_inode);
  if (disk_inode != NULL)
    {
      disk_inode->length = length;
      disk_inode->magic = INODE_MAGIC;
      disk_inode->is_direct = dir;
      /* Matthew driving */
      int i;
      for (i = 0; i < NUM_DIRECT_BLOCKS; i++)
        disk_inode->direct_blocks[i] = INVALID_SECTOR;
      disk_inode->indirect_block = INVALID_SECTOR;
      disk_inode->double_indirect = INVALID_SECTOR;
      if (length > 0)
        {
          int sectors = bytes_to_sectors (length);
          allocate_zeros (sectors, disk_inode, 0);
        }
      block_write (fs_device, sector, disk_inode);
      success = true;
      free (disk_inode);
    }
  return success;
}

/* Reads an inode from SECTOR
   and returns a `struct inode' that contains it.
   Returns a null pointer if memory allocation fails. */
struct inode *
inode_open (block_sector_t sector)
{
  struct list_elem *e;
  struct inode *inode;

  /* Check whether this inode is already open. */
  for (e = list_begin (&open_inodes); e != list_end (&open_inodes);
       e = list_next (e)) 
    {
      inode = list_entry (e, struct inode, elem);
      if (inode->sector == sector) 
        {
          inode_reopen (inode);
          return inode; 
        }
    }

  /* Allocate memory. */
  inode = malloc (sizeof *inode);
  if (inode == NULL)
    return NULL;

  /* Initialize. */
  list_push_front (&open_inodes, &inode->elem);
  inode->sector = sector;
  inode->open_cnt = 1;
  inode->deny_write_cnt = 0;
  inode->removed = false;
  /* John driving */
  inode->writers = 0;
  inode->readers = 0;
  lock_init (&inode->extend_lock);
  lock_init (&inode->read_write_lock);
  cond_init (&inode->readers_cv);
  cond_init (&inode->writers_cv);
  block_read (fs_device, inode->sector, &inode->data);
  return inode;
}

/* Reopens and returns INODE. */
struct inode *
inode_reopen (struct inode *inode)
{
  if (inode != NULL)
    inode->open_cnt++;
  return inode;
}

/* Returns INODE's inode number. */
block_sector_t
inode_get_inumber (const struct inode *inode)
{ 
  return inode->sector;
}

/* Frees the indirect blocks. */
static void
free_ind_block (block_sector_t *indirect)
{
  /* Matthew driving */
  block_sector_t *ind_buffer = (block_sector_t *)malloc (4 * BLOCK_POINTERS);
  block_read (fs_device, *indirect, ind_buffer);
  int i;
  for (i = 0; i < BLOCK_POINTERS; i++)
    {
      if (ind_buffer[i] != INVALID_SECTOR)
        free_map_release (ind_buffer[i], 1);
      else
        break;
    }
  free_map_release (*indirect, 1);
  free (ind_buffer);
}

/* Frees the double indirect block. */
static void
free_doub_block (block_sector_t *double_indirect)
{
  /* Matthew driving */
  block_sector_t *doub_buffer = (block_sector_t *)malloc (4 * BLOCK_POINTERS);
  block_read (fs_device, *double_indirect, doub_buffer);
  int i;
  for (i = 0; i < BLOCK_POINTERS; i++)
    {
      if (doub_buffer[i] != INVALID_SECTOR)
        free_ind_block ((block_sector_t *)doub_buffer[i]);
      else
        break;
    }
  free_map_release (*double_indirect, 1);
  free (doub_buffer);
}

/* Closes INODE and writes it to disk. (Does it?  Check code.)
   If this was the last reference to INODE, frees its memory.
   If INODE was also a removed inode, frees its blocks. */
void
inode_close (struct inode *inode) 
{
  /* Ignore null pointer. */
  if (inode == NULL)
    return;

  /* Release resources if this was the last opener. */
  if (--inode->open_cnt == 0)
    {
      /* Remove from inode list and release lock. */
      list_remove (&inode->elem);
 
      /* Deallocate blocks if removed. */
      if (inode->removed) 
        {
          free_map_release (inode->sector, 1);
          /* Matthew driving */
          int i;
          /* Free direct blocks */
          for (i = 0; i < NUM_DIRECT_BLOCKS; i++)
            {
              if (inode->data.direct_blocks[i] != INVALID_SECTOR)
                free_map_release (inode->data.direct_blocks[i], 1);
              else
                break;
            }
          /* Free indirect block */
          if (inode->data.indirect_block != INVALID_SECTOR)
            free_ind_block ((block_sector_t *)inode->data.indirect_block);
          /* Free doubly indirect block */
          if (inode->data.double_indirect != INVALID_SECTOR)
            free_doub_block ((block_sector_t *)inode->data.double_indirect);
        }

      free (inode); 
    }
}

/* Marks INODE to be deleted when it is closed by the last caller who
   has it open. */
void
inode_remove (struct inode *inode) 
{
  ASSERT (inode != NULL);
  inode->removed = true;
}

/* Reads SIZE bytes from INODE into BUFFER, starting at position OFFSET.
   Returns the number of bytes actually read, which may be less
   than SIZE if an error occurs or end of file is reached. */
off_t
inode_read_at (struct inode *inode, void *buffer_, off_t size, off_t offset) 
{
  /* Matthew, John, and Kirsten driving */
  uint8_t *buffer = buffer_;
  off_t bytes_read = 0;
  uint8_t *bounce = NULL;

  /* Begin read for readers writers problem */
  lock_acquire (&inode->read_write_lock);
  while (inode->writers > 0)
    cond_wait (&inode->writers_cv, &inode->read_write_lock);
  inode->readers++;
  lock_release (&inode->read_write_lock);

  while (size > 0) 
    {
      /* Disk sector to read, starting byte offset within sector. */
      block_sector_t sector_idx = byte_to_sector (inode, offset);
      int sector_ofs = offset % BLOCK_SECTOR_SIZE;

      /* Bytes left in inode, bytes left in sector, lesser of the two. */
      off_t inode_left = inode_length (inode) - offset;
      int sector_left = BLOCK_SECTOR_SIZE - sector_ofs;
      int min_left = inode_left < sector_left ? inode_left : sector_left;

      /* Number of bytes to actually copy out of this sector. */
      int chunk_size = size < min_left ? size : min_left;
      if (chunk_size <= 0)
        break;
      if (sector_ofs == 0 && chunk_size == BLOCK_SECTOR_SIZE)
        {
          /* Read full sector directly into caller's buffer. */
          block_read (fs_device, sector_idx, buffer + bytes_read);
        }
      else 
        {
          /* Read sector into bounce buffer, then partially copy
             into caller's buffer. */
          if (offset > inode->data.length)
            {
              bytes_read = 0;
              break;
            }
          if (bounce == NULL)
            {
              bounce = malloc (BLOCK_SECTOR_SIZE);
              if (bounce == NULL)
                break;
            }
          block_read (fs_device, sector_idx, bounce);
          memcpy (buffer + bytes_read, bounce + sector_ofs, chunk_size);
        }
      
      /* Advance. */
      size -= chunk_size;
      offset += chunk_size;
      bytes_read += chunk_size;

    }
  free (bounce);

  /* End read for readers writers problem */
  lock_acquire (&inode->read_write_lock);
  inode->readers--;
  if (inode->readers == 0)
    cond_signal (&inode->readers_cv, &inode->read_write_lock);
  lock_release (&inode->read_write_lock);

  return bytes_read;
}

/* Writes SIZE bytes from BUFFER into INODE, starting at OFFSET.
   Returns the number of bytes actually written, which may be
   less than SIZE if end of file is reached or an error occurs.
   (Normally a write at end of file would extend the inode, but
   growth is not yet implemented.) */
off_t
inode_write_at (struct inode *inode, const void *buffer_, off_t size,
                off_t offset) 
{
  /* Matthew, John, and Kirsten driving */
  const uint8_t *buffer = buffer_;
  off_t bytes_written = 0;
  uint8_t *bounce = NULL;

  if (inode->deny_write_cnt)
    return 0;

  /* Writing for readers writers problem */
  lock_acquire (&inode->read_write_lock);
  inode->writers++;
  while (inode->readers > 0)
    cond_wait (&inode->readers_cv, &inode->read_write_lock);

  /* In the case that a write is made past the file length the blocks
     are written to zero for anything before the position that will be
     written to. */
  lock_acquire (&inode->extend_lock);
  if (size + offset > inode->data.length)
    {  
      int sectors = bytes_to_sectors (size + offset - inode->data.length);
      int next_block = bytes_to_sectors (inode->data.length);
      allocate_zeros (sectors, &inode->data, next_block);
      inode->data.length = size + offset;
      block_write (fs_device, inode->sector, &inode->data);
    }
  lock_release (&inode->extend_lock);

  while (size > 0) 
    {
      /* Sector to write, starting byte offset within sector. */
      block_sector_t sector_idx = byte_to_sector (inode, offset);

      int sector_ofs = offset % BLOCK_SECTOR_SIZE;

      /* Bytes left in inode, bytes left in sector, lesser of the two. */
      off_t inode_left = inode_length (inode) - offset;
      int sector_left = BLOCK_SECTOR_SIZE - sector_ofs;
      int min_left = inode_left < sector_left ? inode_left : sector_left;

      /* Number of bytes to actually write into this sector. */
      int chunk_size = size < min_left ? size : min_left;
      if (chunk_size <= 0)
        break;

      if (sector_ofs == 0 && chunk_size == BLOCK_SECTOR_SIZE)
        {
          /* Write full sector directly to disk. */
          block_write (fs_device, sector_idx, buffer + bytes_written);
        }
      else 
        {
          /* We need a bounce buffer. */
          if (bounce == NULL) 
            {
              bounce = malloc (BLOCK_SECTOR_SIZE);
              if (bounce == NULL)
                break;
            }

          /* If the sector contains data before or after the chunk
             we're writing, then we need to read in the sector
             first.  Otherwise we start with a sector of all zeros. */
          if (sector_ofs > 0 || chunk_size < sector_left) 
            block_read (fs_device, sector_idx, bounce);
          else
            memset (bounce, 0, BLOCK_SECTOR_SIZE);
          memcpy (bounce + sector_ofs, buffer + bytes_written, chunk_size);
          block_write (fs_device, sector_idx, bounce);
        }

      /* Advance. */
      size -= chunk_size;
      offset += chunk_size;
      bytes_written += chunk_size;
    }
  free (bounce);

  /* Writing for readers writers problem */
  inode->writers--;
  if (inode->writers == 0)
    cond_broadcast (&inode->writers_cv, &inode->read_write_lock);
  else
    cond_signal (&inode->readers_cv, &inode->read_write_lock);
  lock_release (&inode->read_write_lock);

  return bytes_written;
}

/* Disables writes to INODE.
   May be called at most once per inode opener. */
void
inode_deny_write (struct inode *inode) 
{
  inode->deny_write_cnt++;
  ASSERT (inode->deny_write_cnt <= inode->open_cnt);
}

/* Re-enables writes to INODE.
   Must be called once by each inode opener who has called
   inode_deny_write() on the inode, before closing the inode. */
void
inode_allow_write (struct inode *inode) 
{
  ASSERT (inode->deny_write_cnt > 0);
  ASSERT (inode->deny_write_cnt <= inode->open_cnt);
  inode->deny_write_cnt--;
}

/* Returns the length, in bytes, of INODE's data. */
off_t
inode_length (const struct inode *inode)
{
  return inode->data.length;
}

/* Returns true if the inode pointed to is a directory. */
bool
is_directory (struct inode *inode)
{
  /* Kirsten driving */
  return inode->data.is_direct;
}

/* Sets the is_direct bool for the inode. */
void
set_directory (struct inode *inode, bool dir)
{
  /* Kirsten driving */
  inode->data.is_direct = dir;
}
