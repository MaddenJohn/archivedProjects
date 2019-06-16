#ifndef FILESYS_INODE_H
#define FILESYS_INODE_H

#include <stdbool.h>
#include "filesys/off_t.h"
#include "devices/block.h"

struct bitmap;

void inode_init (void);
bool inode_create (block_sector_t, off_t, bool dir);
struct inode *inode_open (block_sector_t);
struct inode *inode_reopen (struct inode *);
block_sector_t inode_get_inumber (const struct inode *);
void inode_close (struct inode *);
void inode_remove (struct inode *);
off_t inode_read_at (struct inode *, void *, off_t size, off_t offset);
off_t inode_write_at (struct inode *, const void *, off_t size, off_t offset);
void inode_deny_write (struct inode *);
void inode_allow_write (struct inode *);
off_t inode_length (const struct inode *);
bool is_directory (struct inode *inode);
void set_directory (struct inode *inode, bool dir);
struct dir *get_last_dir (const char *path);
int inode_open_count (struct inode *inode);

void inode_set_parent (block_sector_t par, struct inode *ch);
block_sector_t inode_get_parent (struct inode *dir);

void inode_chld_increment (struct inode* inode);
void inode_chld_decrement (struct inode* inode);
bool inode_has_entries (struct inode* inode);
int inode_num_entries (struct inode* inode);


#endif /* filesys/inode.h */
