#include "filesys/filesys.h"
#include <debug.h>
#include <stdio.h>
#include <string.h>
#include "filesys/file.h"
#include "filesys/free-map.h"
#include "filesys/inode.h"
#include "filesys/directory.h"
#include "threads/thread.h"

/* Partition that contains the file system. */
struct block *fs_device;

static void do_format (void);

/* Initializes the file system module.
   If FORMAT is true, reformats the file system. */
void
filesys_init (bool format) 
{
  fs_device = block_get_role (BLOCK_FILESYS);
  if (fs_device == NULL)
    PANIC ("No file system device found, can't initialize file system.");

  inode_init ();
  free_map_init ();

  if (format) 
    do_format ();

  free_map_open ();
}

/* Shuts down the file system module, writing any unwritten data
   to disk. */
void
filesys_done (void) 
{
  free_map_close ();
}
 
/* Creates a file named NAME with the given INITIAL_SIZE.
   Returns true if successful, false otherwise.
   Fails if a file named NAME already exists,
   or if internal memory allocation fails. */
bool
filesys_create (const char *name, off_t initial_size, bool is_dir) 
{
  /* John driving */
  block_sector_t inode_sector = 0;
  struct dir *dir = get_last_dir (name);
  const char *new_name = NULL;
  if (dir != NULL)
  {
    new_name = strrchr (name, '/');
    if (new_name == NULL)
      new_name = name;
    else 
      new_name++;
  }
  ASSERT(dir != NULL);
  bool success = (dir != NULL
                  && free_map_allocate ( 1, &inode_sector)
                  && inode_create (inode_sector, initial_size, is_dir)
                  && dir_add (dir, new_name, inode_sector));
  struct dir *ch_dir  = dir_open (inode_open (inode_sector));//get child directory
  inode_set_parent (inode_get_inumber (dir_get_inode (dir)), dir_get_inode (ch_dir));
  dir_close (ch_dir);

  if (!success && inode_sector != FREE_MAP_SECTOR)
    free_map_release (inode_sector, 1);
  dir_close (dir);
  return success;
}

/* Opens the file with the given NAME.
   Returns the new file if successful or a null pointer
   otherwise.
   Fails if no file named NAME exists,
   or if an internal memory allocation fails. */
void *
filesys_open (const char *name)
{
  // 
  /* John, Matthew, and Kirsten driving */
  struct dir *dir = get_last_dir (name);
  // if(strcmp (name,"tar") ==0  ||strcmp (name,"fs.tar") ==0)
  // {
  //   printf("opening from root for tar\n");
  //   dir_close (dir);
  //   dir = dir_open_root ();
  // }
  const char *new_name = NULL;
  bool success = false;
  struct inode *inode = NULL;

  if (dir != NULL)
  {
    if (strcmp (name, ".") == 0)
      return dir_open (inode_open (thread_current ()->dir_inode));
    else if (strcmp (name, "..") == 0)
      return dir_open (inode_open (thread_current ()->parent->dir_inode));
    new_name = strrchr (name, '/');
    if (new_name == NULL)
      new_name = name;
    else if (strcmp (new_name, "/") == 0)
      return dir;
    else 
      new_name++;
    
    success = dir_lookup (dir, new_name, &inode);
    if (!success)
    {
      // printf("FS Open name: %s  TC: %s  ***************\n",name ,thread_current ()->name);
       return NULL;
    }
     
  }
  else
    return NULL;
  dir_close (dir);
 
  if (is_directory (inode))
    return dir_open (inode);

  return file_open (inode);
}

/* Deletes the file named NAME.
   Returns true if successful, false on failure.
   Fails if no file named NAME exists,
   or if an internal memory allocation fails. */
bool
filesys_remove (const char *name) 
{
  /* John driving */
  struct dir *dir = get_last_dir (name);
  const char *new_name = strrchr (name, '/');
  if (new_name == NULL)
    new_name = name;
  else if (*new_name == '/')
    new_name++;
  else if (strcmp (new_name, ".") == 0)
    dir_readdir (dir, new_name);
  else if (strcmp (new_name, "..") == 0)
    return false;
  bool success = (dir != NULL && dir_remove (dir, new_name));
  dir_close (dir);  
  return success;
}

/* Formats the file system. */
static void
do_format (void)
{
  printf ("Formatting file system...");
  free_map_create ();
  if (!dir_create (ROOT_DIR_SECTOR, 16))
    PANIC ("root directory creation failed");
  free_map_close ();
  printf ("done.\n");
}
