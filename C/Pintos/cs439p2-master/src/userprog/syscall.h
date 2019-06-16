#include <stdbool.h>
#include <stdint.h>
#ifndef USERPROG_SYSCALL_H
#define USERPROG_SYSCALL_H

void syscall_init (void);
bool check_pointer (const void *buffer);

#endif /* userprog/syscall.h */
