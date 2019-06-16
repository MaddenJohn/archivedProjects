#ifndef USERPROG_SYSCALL_H
#define USERPROG_SYSCALL_H
#include <list.h>
#include "threads/thread.h"
void syscall_init (void);
void close_all_files(void);
// Jose driving now
struct process{
	pid_t pid;
	struct thread *th;
	int exitStatus;
	bool success;
	struct thread *parent; 
	struct list_elem e;
	struct semaphore exited;         //
    struct semaphore success_sema;   //
    int dealocated;			         //will be null if memory is freed	
};

// Alec driving now
struct filefd{
  struct file* openfile;    // Carries the open file.
  int fd;                   // The file's file descriptor.
  struct list_elem file_e;  // list_elem for the processes list.
};

#endif /* userprog/syscall.h */
