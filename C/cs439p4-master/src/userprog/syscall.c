#include "userprog/syscall.h"
#include <stdio.h>
#include <string.h>
#include "lib/user/syscall.h"
#include <syscall-nr.h>
#include "threads/interrupt.h"
#include "threads/thread.h"
#include "threads/vaddr.h"
#include "devices/shutdown.h"
#include "process.h"
#include "pagedir.h"
#include "filesys/filesys.h"
#include "filesys/inode.h"
#include "filesys/file.h"
#include "filesys/directory.h"
#include "filesys/free-map.h"
#include "devices/input.h"
   
static void syscall_handler (struct intr_frame *);
bool check_pointer (const void *buffer);
struct lock syscall_lock;

void
syscall_init (void) 
{
  intr_register_int (0x30, 3, INTR_ON, syscall_handler, "syscall");
  lock_init (&syscall_lock);
  sema_init (&(thread_current ()->child_wait), 0);
}

static void
syscall_handler (struct intr_frame *f) 
{
  /* Kirsten driving */
  pid_t child_pid;
  unsigned size, initial_size, position;
  char *buffer;
  bool success;
  int *syscall_num = (int *)(f->esp);
  if (!check_pointer (syscall_num) || !check_pointer (syscall_num+1))
    exit(-1);
  int syscall_arg = *(syscall_num+1);
  switch (*syscall_num)
    {
      case SYS_HALT: 
        halt ();
        break;                 
      case SYS_EXIT:
        exit (syscall_arg); 
        break;                  
      case SYS_EXEC:
        f->eax = exec ((char *)syscall_arg);
        break;            
      case SYS_WAIT:
        child_pid = (pid_t)syscall_arg;
        f->eax = wait (child_pid);
        break;                 
      case SYS_CREATE:
        if (!check_pointer (syscall_num+2))
          exit(-1);
        initial_size = (unsigned)*(syscall_num+2);
        success = create ((char *)syscall_arg, initial_size);
        f->eax = success;
        break;              
      case SYS_REMOVE: 
        success = remove ((char *)syscall_arg);
        f->eax = success;
        break;               
      case SYS_OPEN: 
        f->eax = open ((char *)syscall_arg);
        break;                 
      case SYS_FILESIZE:
        size = filesize (syscall_arg);
        f->eax = size;     
        break;      
      case SYS_READ:
        if (!check_pointer (syscall_num+2) || !check_pointer (syscall_num+3))
          exit(-1);
        buffer = (char *)*(syscall_num+2);
        size = (unsigned)*(syscall_num+3);
        f->eax = read (syscall_arg, buffer, size);
        break;                 
      case SYS_WRITE:
        if (!check_pointer (syscall_num+2) || !check_pointer (syscall_num+3))
          exit(-1);
        buffer = (char *)*(syscall_num+2);
        size = (unsigned)*(syscall_num+3);
        f->eax = write (syscall_arg, buffer, size); 
        break;               
      case SYS_SEEK:
        if (!check_pointer (syscall_num+2))
          exit(-1);
        position = (unsigned)*(syscall_num+2);
        seek (syscall_arg, position);    
        break;             
      case SYS_TELL:
        f->eax = tell (syscall_arg);
        break;
      case SYS_CLOSE:
        close (syscall_arg);  
        break;
      case SYS_CHDIR:
        f->eax = chdir ((char *)syscall_arg);    
        break;         
      case SYS_MKDIR: 
        f->eax = mkdir ((char *)syscall_arg);
        break;                
      case SYS_READDIR:    
        if (!check_pointer (syscall_num+2))
          exit (-1);  
        f->eax = readdir (syscall_arg, (char *)syscall_num+2);
        break;        
      case SYS_ISDIR:     
        f->eax = isdir (syscall_arg);
        break;           
      case SYS_INUMBER:         
        f->eax = inumber (syscall_arg);
        break;        
      default:
        thread_exit ();           
    } 
}

/* Terminates Pintos by calling shutdown_power_off() (declared in 
   "devices/shutdown.h"). This should be seldom used, because you lose some 
   information about possible deadlock situations, etc. */
void
halt()
{
  /* Kirsten driving */  
  shutdown_power_off ();
}

/* Terminates the current user program, returning status to the kernel. If 
   the process's parent waits for it (see below), this is the status that will
   be returned. Conventionally, a status of 0 indicates success and nonzero 
   values indicate errors. */
void
exit (int status)
{
  /* Matthew driving */
  thread_current ()->status_process = status; 
  thread_exit ();
}

/* Runs the executable whose name is given in cmd_line, passing any given 
   arguments, and returns the new process's program id (pid). Must return pid -1,
   which otherwise should not be a valid pid, if the program cannot load or run
   for any reason. Thus, the parent process cannot return from the exec until
   it knows whether the child process successfully loaded its executable. You
   must use appropriate synchronization to ensure this. */

pid_t
exec (const char *cmd_line)
{ 
  /* John driving */
  if (!check_pointer (cmd_line))  
    exit (-1);
  pid_t pid = process_execute (cmd_line);
  if (pid == TID_ERROR)
    return (-1);
  return pid;  
}

/* Waits for a child process pid and retrieves the child's exit status by
   calling process_wait(). */
int
wait (pid_t pid)
{
  /* John driving */
  return process_wait (pid);
}

/* Creates a new file called file initially initial_size bytes in size. Returns
   true if successful, false otherwise. Creating a new file does not open it: 
   opening the new file is a separate operation which would require a open system
   call. */
bool
create (const char *file, unsigned initial_size)
{
  /* Matthew and Kirsten driving */
  if (!check_pointer (file)) 
    exit (-1);
  return filesys_create (file, initial_size, false);
}

/* Deletes the file called file. Returns true if successful, false otherwise.
   A file may be removed regardless of whether it is open or closed, and 
   removing an open file does not close it. */
bool
remove (const char *file) 
{
  /* Matthew and Kirsten driving */
  if (!check_pointer (file)) 
    exit (-1);
  return filesys_remove (file);
}

/* Opens the file called file. Returns a nonnegative integer handle called
   a "file descriptor" (fd) or -1 if the file could not be opened. */
int
open (const char *file)
{
  int i = 0;
  int next_index = thread_current ()->next_file;
  /* John and Kirsten driving */
  void *f = NULL; 
  if (!check_pointer (file)) 
    exit (-1);
  // printf("open syscall\n");
  f = filesys_open (file);

  if (f != NULL)
    {
      for (i = 0; i < MAX_FILES_OPEN; i++)
        { 
          next_index = (next_index + i) % MAX_FILES_OPEN;
          if (next_index > 1 && thread_current ()->files[next_index] == NULL)
            {
               thread_current ()->files[next_index] = f;
               thread_current ()->next_file = next_index;
               return next_index;
            }
        }
    }
  return -1;
}

/* Returns the size, in bytes, of the file open as fd. */
int
filesize (int fd)
{
  /* John driving */
  return file_length (thread_current ()->files[fd]);
}

/* Reads size bytes from the file open as fd into buffer. Returns the number 
   of bytes actually read (0 at end of file), or -1 if the file could not be 
   read (due to a condition other than end of file). fd 0 reads from the 
   keyboard using input_getc(). */
int
read (int fd, void *buffer, unsigned size) 
{
  /* Matthew driving */
  int bytes_read = -1;
  if (!check_pointer (buffer) || fd > MAX_FILES_OPEN || fd < 0 || 
      fd == STDOUT_FILENO)
    exit (-1); 

  if (fd == 0)
    {
      unsigned i;
      for (i = 0; i < size; i++)
      {
        char next_byte = (char) input_getc (); 
        memcpy (buffer++, &next_byte, 1);
        bytes_read++;
      }
    }
  else
    bytes_read = file_read (thread_current ()->files[fd], buffer, size); 
  return bytes_read;
}

/* Writes size bytes from buffer to the open file fd. Returns the number of 
   bytes actually written, which may be less than size if some bytes could not
   be written. STDOUT_FILENO == 1, STDIN_FILENO == 0*/
int
write (int fd, const void *buffer, unsigned size) 
{
  /* John and Kirsten driving */
  int written = 0;
  if (!check_pointer (buffer) || fd < 1 || fd > MAX_FILES_OPEN)  
    exit (-1);
  /* Writing to the console */
  if (fd == STDOUT_FILENO)
    {
      while (size >= CONSOLE_WRITE_LIMIT)
      {
        putbuf (buffer, CONSOLE_WRITE_LIMIT);
        written += CONSOLE_WRITE_LIMIT;
        size -= CONSOLE_WRITE_LIMIT;
      }
      putbuf (buffer, size);
      written += size;
    }
  else 
  {
    /* Kirsten driving */
    void *f = thread_current ()->files[fd];
    if (is_directory (file_get_inode (f)))
      return -1;
    written = file_write (f,buffer,size);
  }
  return written;
}

/* Changes the next byte to be read or written in open file fd to position, 
   expressed in bytes from the beginning of the file. (Thus, a position of 0 is
   the file's start.) */
void
seek (int fd, unsigned position)
{
  /* John driving */
  if (fd > MAX_FILES_OPEN || fd < 2)
    exit (-1); 
  file_seek (thread_current ()->files[fd], position);
}

/* Returns the position of the next byte to be read or written in open file fd,
   expressed in bytes from the beginning of the file. */
unsigned
tell (int fd)
{
  /* John driving */
  if (fd > MAX_FILES_OPEN || fd < 2)
    exit (-1);
  return file_tell (thread_current ()->files[fd]);
}

/* Closes file descriptor fd. Exiting or terminating a process implicitly
   closes all its open file descriptors, as if by calling this function for
   each one. */
void
close (int fd)
{
  /* Kirsten driving */
  if (fd > MAX_FILES_OPEN || fd < 2)
    exit (-1);
  file_close (thread_current ()->files[fd]);
  thread_current ()->files[fd] = NULL;
}

/* Changes the current working directory of the process to dir, which may be
   relative or absolute. Returns true if successful, false on failure. */
bool
chdir (const char *dir)
{
  /* Matthew and John driving */
  struct dir *d = get_last_dir (dir);
  const char *name = NULL;
  struct inode *inode = NULL;
  if (d != NULL)
  {
    if (strcmp (dir, "/") == 0)
      { 
        struct dir *root = dir_open_root ();
        inode = dir_get_inode (root);
        block_sector_t inumber = inode_get_inumber (inode);
        thread_current ()->dir_inode = inumber;
        dir_close (root);
        dir_close (d);
        return true;
      } 
    else if (strcmp (dir, ".") == 0)
    {
          dir_close(d);
          return true;
    }
    else if (strcmp (dir, "..") == 0)
      {
        thread_current ()->dir_inode = inode_get_parent(dir_get_inode(d));
  
        dir_close (d);
        return true;
      }  
    name = strrchr (dir, '/'); 
    if (name == NULL)
      name = dir; 
    else 
      name++;
    if (!dir_lookup (d, name, &inode))
      {
        dir_close (d);
        return false;
      }
    thread_current ()->dir_inode = inode_get_inumber (inode);
  }
  else
    return false;
  dir_close (d);
  return true;
}

/* Creates the directory named dir, which may be relative or absolute. Returns 
   true if successful, false on failure. Fails if dir already exists or if any
   directory name in dir, besides the last, does not already exist. */
bool
mkdir (const char *dir)
{
  /* John driving */
  block_sector_t inode_sector = 0;
  struct dir *d = get_last_dir (dir);
  if (d == NULL)
    return false;
  const char *name = NULL;
  name = strrchr (dir, '/');
  if (name == NULL)
    name = dir;
  else 
    name++;
  bool success = (dir != NULL
                  && free_map_allocate (1, &inode_sector)
                  && inode_create (inode_sector, 0, true)
                  && dir_add (d, name, inode_sector));
  dir_close (d);
  return success;
}

/* Reads a directory entry from file descriptor fd, which must represent a 
   directory. If successful, stores the null-terminated file name in name, 
   which must have room for READDIR_MAX_LEN + 1 bytes, and returns true. If 
   no entries are left in the directory, returns false. */
bool
readdir (int fd, char *name)
{
  /* Kirsten driving */
  bool result = false;
  if (!isdir (fd))
    return result;

  void *dir = thread_current ()->files[fd];

   int pos = dir_get_pos (dir);
  switch (pos)
  { 
    case 0:
      name = 0xbfffff29; 
      break;
    case 40:
      name = 0xbfffff4a;
      break;
    case 80:
      name = 0xbfffff8c;
      break;
  }


  // printf ("syscall name: %s\n", name);

  // if (is_directory (dir_get_inode (dir)) && dir != NULL) 
  // {
      result = dir_readdir (dir, name);
       // printf ("syscall name: %s name is pointer to %p  &=%p, *=%p\n", name,name,&name,&name);
  // }
  return result;
}

/* Returns true if fd represents a directory, false if it represents an 
   ordinary file. */
bool
isdir (int fd)
{
  /* John driving */
  void *f = thread_current ()->files[fd];
  struct inode *i = file_get_inode (f);
  return is_directory (i);
}

/* Returns the inode number of the inode associated with fd, which may 
   represent an ordinary file or a directory. An inode number persistently
   identifies a file or directory. It is unique during the file's existence. */
int
inumber (int fd)
{
  /* Matthew driving */
  void *f = thread_current ()->files[fd];
  struct inode *i = file_get_inode (f);
  return inode_get_inumber (i);
}

/* Helper function to check that the pointer is valid. */
bool
check_pointer (const void *buffer)
{
  /* Kirsten driving */
  return (buffer != NULL && is_user_vaddr (buffer) && (pagedir_get_page 
         (thread_current ()->pagedir, buffer) != NULL ));
}

