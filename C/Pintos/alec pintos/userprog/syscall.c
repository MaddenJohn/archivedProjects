#include "userprog/syscall.h"
#include <stdio.h>
#include <syscall-nr.h>
#include "threads/interrupt.h"
#include "threads/thread.h"
#include "userprog/process.h"
#include "threads/synch.h"
#include "userprog/pagedir.h"
#include "filesys/filesys.h"
#include "threads/vaddr.h"
#include <unistd.h>

// Jose driving now
void halt (void);
void exit (int );
pid_t exec(const char *) ;
int wait (pid_t) ;
bool create (const char *, unsigned);
bool remove (const char *);
int open (const char *);
int filesize (int ) ;
int read (int, void *, unsigned) ;
int write (int, const void *, unsigned);
void seek (int, unsigned);
unsigned tell (int) ;
void close (int) ;

struct lock sys_lock;
static void syscall_handler (struct intr_frame *);



/*Verifies that a pointer is both below PHYS_BASE and references a page, otherwise exit the process
*/
bool  // Jose driving now 
verify_user_pointer(void *p){
	
	if(p == NULL  ||  p >= PHYS_BASE || p < 0x08048000 || pagedir_get_page(thread_current()->pagedir,p) == NULL){	
		
		printf ("%s: exit(%d)\n",thread_name(), thread_current()->pr->exitStatus=-1);
		
		
		sema_up(&thread_current()->pr->exited);
		
		thread_exit();
		return false;
	}

	return true;
}


void close_all_files(void){
  struct thread *cur= thread_current();
   
 
    struct list_elem *e;
    lock_acquire(&sys_lock);
    for (e = list_begin (&cur->files); e != list_end (&cur->files);e = list_next (e))
    {
      struct filefd *ffd = list_entry(e, struct filefd, file_e);
      struct file* file= ffd->openfile;
    
      file_close(file);
      list_remove(&ffd->file_e);
      free(ffd);
      
      
	  
      
      
	  

    }

   lock_release(&sys_lock);
   

}




/*Retrieves a filefd from an fd argument by iterating through the processes list of filefds.
  If not found return NULL to signify an error.
*/
struct filefd* // Alec driving now
get_filefd(int reqfd){

	struct thread *cur = thread_current();	
    struct list_elem *e;

    for (e = list_begin (&cur->files); e != list_end (&cur->files);e = list_next (e))
    {
    	struct filefd *t = list_entry (e, struct filefd, file_e);

		if(t->fd == reqfd){
			return t;
	  	} 
    }

    return NULL;
}





void
syscall_init (void) 
{
	lock_init(&sys_lock);
	intr_register_int (0x30, 3, INTR_ON, syscall_handler, "syscall");
}

/* Retrieves the system call number from frame f and redirects to the corresponding system call function
   Verifies argument pointers and sets eax when neccessary.
*/
static void
syscall_handler (struct intr_frame *f UNUSED)
{
	// Jose and Alec driving now
	int *myEsp = (int *)f->esp;
	
	verify_user_pointer(myEsp);
    verify_user_pointer(myEsp+1);

	switch(*(myEsp)){ 
	    // Alec driving now    
		case SYS_HALT       :   halt(); 
								break;

		case SYS_EXIT       :    exit((int) *(myEsp+1));
								break;

		case SYS_EXEC       :   f->eax = exec((char *)*(myEsp+1)); 
								break;
        // Jose driving now
		case SYS_WAIT       :   f->eax = wait((char *)*(myEsp+1)); 
								break;

		case SYS_CREATE     :   verify_user_pointer(myEsp+2); 
								f->eax = create((char *)*(myEsp+1), (unsigned)*(myEsp+2)); 
								break;

		case SYS_REMOVE     :   f->eax = remove((char *)*(myEsp+1)); 
								break;
        // Jose and Alec driving now
		case SYS_OPEN       :	f->eax = open ((char *)*(myEsp+1)); 
								break;

		case SYS_FILESIZE   :	f->eax = filesize ((int) *(myEsp+1)); 
								break;

		case SYS_READ       :	f->eax = read ((int)*(myEsp+1), (void *)*(myEsp+2), (unsigned)*(myEsp+3)); 
								break;

		case SYS_WRITE      :	verify_user_pointer(myEsp+2);
								verify_user_pointer(myEsp+3);
								f->eax = write ((int)*(myEsp+1), (void *)*(myEsp+2), (unsigned)*(myEsp+3)); 
								break;

		case SYS_SEEK       :	verify_user_pointer(myEsp+2); 
								seek ((int) *(myEsp+1), (unsigned)*(myEsp+2)); 
								break;

		case SYS_TELL       :	f->eax = tell ((int)*(myEsp+1)); 
								break;

		case SYS_CLOSE      :	close ((int)*(myEsp+1)); 
								break;
	}
}

/* Terminates pintos.
*/
void 
halt(){
	// Alec driving now
	shutdown_power_off();
}

/* Terminates the process with thread_exit(). The process's exitStatus variable is set so that
it may be checked by the parent processes may. 
*/
void 
exit (int status){
	// Jose driving now
	struct thread* curthread = thread_current();

	curthread->pr->exitStatus=status;

	printf ("%s: exit(%d)\n",thread_name(), status);
	
    
	
    sema_up(&curthread->pr->exited);
    
	thread_exit ();
}

/* Starts a new process by calling process_execute and if succesful will return the childs pid.
Semaphore success_sema was used for proper synchronization in case load of process is unsuccesful.
*/
pid_t 
exec(const char *cmd_line){
    // Jose driving now
	pid_t child_pid;
	struct process *childP;

	verify_user_pointer(cmd_line);

	char * args = palloc_get_page(0);
	strlcpy(args, cmd_line,PGSIZE);

	child_pid = process_execute(args);

	palloc_free_page(args);

	childP = getChild(child_pid);

	if(childP->dealocated == 12345){
		sema_down(&childP->success_sema);
	}else{
		return -1;
	}
	
	if(!childP->success){		
		return -1;
	}else{	
		return child_pid;
	}
}

/* Waits for a process to terminate by calling process_wait.
*/
int 
wait (tid_t pid) {
	// Jose driving now
	int exitstatus = process_wait(pid);

	return exitstatus;
}

/*Verifies the pointer, then creates a file by calling filesys_create.
*/
bool 
create (const char *file, unsigned initial_size) {
	// Alec driving now
	bool result;
    verify_user_pointer(file);

	lock_acquire(&sys_lock);
	result = filesys_create (file, initial_size);
	lock_release(&sys_lock);

	return result;
}

/* Verifies the pointer, then removes the file by calling filesys_remove.
*/
bool 
remove (const char *file) {
	// Jose driving now
	bool result;
	verify_user_pointer(file);

	lock_acquire(&sys_lock);
	result = filesys_remove (file);
	lock_release(&sys_lock);

	return result;
} 

/* Allocates the space for a new filefd struct to be added to the process's files list.
If the pointer is valid and file_open does not return NULL then set the new filefd's file
pointer to the newly opened file. The currently opened file's fd will start at 2 and then
iterate by 1 for each file opened after that. After the new filefd's variables have been set
push it onto the processe's files list.
*/
int 
open (const char *file) {
    // Alec driving now
	struct filefd *openfd = malloc(sizeof(struct filefd));
	verify_user_pointer(file);

	lock_acquire(&sys_lock);

	struct file *tempfile = filesys_open(file);

	if(tempfile == NULL){
		lock_release(&sys_lock);
		return -1;
	}

	struct thread *cur = thread_current();
	openfd->openfile = tempfile;
    openfd->fd = cur->topfd + 1;
    cur->topfd = openfd->fd;
    list_push_front(&cur->files,&openfd->file_e);

	lock_release(&sys_lock);

	return openfd->fd;
}

/*Retrieves the appropriate file with get_filefd. If found return the result of file_length.
*/
int 
filesize (int fd){
	// Alec driving now
	int length;

	lock_acquire(&sys_lock);

	struct filefd *tempffd = get_filefd(fd);

	if(tempffd == NULL){
		lock_release(&sys_lock);
		return -1;
	}

	length = file_length(tempffd->openfile);

	lock_release(&sys_lock);

	return length;
}

/* Verifies buffer for user pointer. Retrieves the file open under fd using
get_file. Reads the specified amount of bytes from the fd's file into the buffer.
*/
int 
read (int fd, void *buffer, unsigned size) {
	// Jose driving now
	int result = 0;
	verify_user_pointer(buffer);
	
	lock_acquire(&sys_lock);

	if(fd==0){
		char *ptr;
		for(ptr = buffer; ptr<buffer+size; ptr++){
			result++;
			*ptr = input_getc();
		}

		lock_release(&sys_lock);
      	return result;
	}

	struct filefd *tempffd = get_filefd(fd);

	if(tempffd == NULL){
		lock_release(&sys_lock);
		return -1;
	}

	result = file_read(tempffd->openfile, buffer, size);

    lock_release(&sys_lock);
   
	return result;
}

/* Verifies buffer for user pointer. Retrieves the file open under fd using
get_file. Writes the specified amount of bytes from the fd's file into the buffer.
*/
int 
write (int fd, const void *buffer, unsigned size) {
	// Jose driving now
	int result;
	verify_user_pointer(buffer);
	
	lock_acquire(&sys_lock);

	if(fd == 1){
		putbuf(buffer, size);

		lock_release(&sys_lock);
      	return size;
	}

	struct filefd *tempffd = get_filefd(fd);

	if(tempffd == NULL){
		lock_release(&sys_lock);
		return -1;
	}

	result= file_write(tempffd->openfile, buffer, size);

    lock_release(&sys_lock);

	return result;
}

/* Retrieves the appropriate file with get_filefd, then, if found, calls file_seek with that 
file and the signified position.
*/
void 
seek (int fd, unsigned position){
	// Alec driving now
	lock_acquire(&sys_lock);

	struct filefd *tempffd = get_filefd(fd);

	if(tempffd != NULL){
		file_seek(tempffd->openfile,position);
	}

	lock_release(&sys_lock);
}

/*Retrieves the appropriate file with get_filefd. If the file is not found return -1 otherwise, 
return the result file_tell.
*/
unsigned 
tell (int fd) {
	// Alec driving now
	int nextPos;

	lock_acquire(&sys_lock);

	struct filefd *tempffd = get_filefd(fd);

	if(tempffd == NULL){
		lock_release(&sys_lock);
		return -1;
	}

	nextPos = file_tell(tempffd->openfile);

	lock_release(&sys_lock);

	return nextPos;
}

/*Retrieves the appropriate file with get_filefd. If the file is found, close it with file_close,
remove the file from the processs files list, and free the space taken by the file's filefd struct. 
*/
void 
close (int fd) {
    // Jose driving now
	lock_acquire(&sys_lock);
 
	struct filefd *tempffd = get_filefd(fd);

	if(tempffd != NULL){

		file_close(tempffd->openfile);

		list_remove(&tempffd->file_e);
		free(tempffd);
	}

	lock_release(&sys_lock);
}
