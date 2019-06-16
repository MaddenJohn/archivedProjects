#include "userprog/syscall.h"
#include <stdio.h>
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

static void syscall_handler (struct intr_frame *);
bool check_pointer (const void *buffer);
int open_count = 1;
struct lock syscall_lock;
struct lock file_lock;

void
syscall_init (void) 
{
  intr_register_int (0x30, 3, INTR_ON, syscall_handler, "syscall");
  lock_init (&syscall_lock);
  lock_init (&file_lock);
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
  if (!check_pointer(syscall_num))
    exit(-1);
  int syscall_arg = *(syscall_num+1);
  //printf("in handler syscall_arg: %d\n",*syscall_num);
  switch (*syscall_num)
    {
      //printf("%d\n", );
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
        buffer = (char *)*(syscall_num+2);
        size = (unsigned)*(syscall_num+3);
        f->eax = read (syscall_arg, buffer, size);
        //printf("read returned %d\n", f->eax);
        break;                 
      case SYS_WRITE:
        //printf("writing\n");
        buffer = (char *)*(syscall_num+2);
        size = (unsigned)*(syscall_num+3);
        f->eax = write (syscall_arg, buffer, size); 
        //printf("done writing\n");
        break;               
      case SYS_SEEK:
        position = (unsigned)*(syscall_num+2);
        seek (syscall_arg, position);    
        break;             
      case SYS_TELL:
        tell (syscall_arg);
        break;
      case SYS_CLOSE:
        close (syscall_arg);  
        break;
      default:
        //exit(-1);
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
  //printf("&status: %d\n",(unsigned)status);
   if (status < 0)
     status = -1;
  
  thread_current ()->status_process = status; 
  thread_exit ();
}

bool
check_file (const char *file)
{
  bool file_exist = false;
  struct dir *dir = dir_open_root ();
  struct inode *inode = NULL;

  if (dir != NULL)
    file_exist = dir_lookup (dir, file, &inode);
  dir_close (dir);

  return file_exist;
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
  //check cmd_line
  if (!check_pointer (cmd_line))  
    exit (-1); 
  /* FIX */
  // if (!check_file (cmd_line))
  //    return (-1);
  /* use lock to ensure parent does not return from exec until it knows
     child process successfully loaded executable. */
  /* John driving */
  lock_acquire (&syscall_lock);
  pid_t pid = process_execute (cmd_line);

  lock_release (&syscall_lock);
  //printf("SYSCALL: ------   WANT PID == -1, pid: %d\n", pid);
  if (pid == TID_ERROR)
    exit (-1);
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
  bool result;
  //check file
  if (!check_pointer (file)) 
    exit (-1);

  lock_acquire (&file_lock);//mr
  result = filesys_create (file, initial_size); //kt
  lock_release (&file_lock);//mr
  return result; //mr
}

/* Deletes the file called file. Returns true if successful, false otherwise.
   A file may be removed regardless of whether it is open or closed, and 
   removing an open file does not close it. */
bool
remove (const char *file) 
{
  bool result;//mr
  //check file
  if (!check_pointer (file)) 
    exit (-1);

  //might need a lock
  lock_acquire (&file_lock);//mr
  result = filesys_remove (file); //kt
  lock_release (&file_lock);//mr
  return result; //mr
}

/* Opens the file called file. Returns a nonnegative integer handle called
   a "file descriptor" (fd) or -1 if the file could not be opened. */
int
open (const char *file)
{
  //check file
  struct file *f = NULL; 
  if (!check_pointer (file)) 
    exit (-1);
  /* Kirsten driving */

  lock_acquire (&file_lock);
  f = filesys_open (file);
  lock_release (&file_lock);
  if(f != NULL)
    { 
      open_count++;
      //file_deny_write (struct file *file) 
      thread_current ()->files[thread_current ()->next_file] = f;
      thread_current ()->next_file++;
      return open_count;
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

  int bytes_read = -1;
  //check buffer
  if (!check_pointer (buffer) || fd > 128 || fd < 0 || fd == 1) 
    exit (-1);

  lock_acquire (&file_lock);
  //printf("fd: %d  size: %d\n",fd,size);
  if(fd == 0)
    bytes_read = file_read (input_getc (), buffer, size);
  else
    bytes_read = file_read (thread_current ()->files[fd], buffer, size); 
   
  lock_release (&file_lock);
  //printf("bytes_read %d\n", bytes_read);
  return bytes_read;
}

/* Writes size bytes from buffer to the open file fd. Returns the number of 
   bytes actually written, which may be less than size if some bytes could not
   be written. STDOUT_FILENO == 1, STDIN_FILENO == 0*/
int
write (int fd, const void *buffer, unsigned size) 
{
  //printf("in write  fd: %d  buffer %s   size %d\n", fd,buffer,size);
  /* John and Kirsten driving */
  int written = 0;
  /* writing to the console */
  if (!check_pointer (buffer) || fd < 1 || fd > 128) 
      exit (-1);
  lock_acquire (&file_lock);  
  if (fd == STDOUT_FILENO)
    {
      if (size < 256)
        {
          putbuf (buffer, size);
          written = size;
        }
      else 
        {
          putbuf (buffer, 256);
          written = 256;
        } 
    }
  else 
  {
    /* Ensure that the executable of a running process cannot be
   modified. */
  // if(true)

    written = file_write (thread_current ()->files[fd],buffer,size);
    ////////////////////////////////////////////////////////////////////////////////////////////////printf ("trying to write, written: %d\n", written);
    //if(written == 0)

  }
  lock_release (&file_lock); 
  return written;
}

/* Changes the next byte to be read or written in open file fd to position, 
   expressed in bytes from the beginning of the file. (Thus, a position of 0 is
   the file's start.) */
void
seek (int fd, unsigned position)
{
  // if(thread_current ()->files[fd] == NULL)
  //   exit(-1);
  
  lock_acquire (&file_lock); 
  file_seek (thread_current ()->files[fd], position);
  lock_release (&file_lock); 
}

/* Returns the position of the next byte to be read or written in open file fd,
   expressed in bytes from the beginning of the file. */
unsigned
tell (int fd)
{
  return file_tell (thread_current ()->files[fd]);
}

/* Closes file descriptor fd. Exiting or terminating a process implicitly
   closes all its open file descriptors, as if by calling this function for
   each one. */
void
close (int fd)
{
  if (fd > 128 || fd < 2)
    exit (-1);
  lock_acquire (&file_lock);
  file_close (thread_current ()->files[fd]);
  thread_current ()->files[fd] = NULL;
  lock_release (&file_lock); 
}

bool
check_pointer (const void *buffer)
{
  return (buffer != NULL && is_user_vaddr (buffer) && (pagedir_get_page (thread_current ()->pagedir, buffer) != NULL ));
}
