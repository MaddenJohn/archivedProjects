#include <stdbool.h>
#include <stdint.h>
#ifndef USERPROG_SYSCALL_H
#define USERPROG_SYSCALL_H
#define CONSOLE_WRITE_LIMIT 128
#define MAX_FILES_OPEN 128

void syscall_init (void);
bool check_pointer (const void *buffer);
void exit (int status);

#endif /* userprog/syscall.h */
