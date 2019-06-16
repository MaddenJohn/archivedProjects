#ifndef FILESYS_FSUTIL_H
#define FILESYS_FSUTIL_H

#include "filesys/directory.h"

void fsutil_ls (char **argv);
void fsutil_cat (char **argv);
void fsutil_rm (char **argv);
void fsutil_extract (char **argv);
void fsutil_append (char **argv);
void fsutil_ls_dirarg (struct dir *dir); 

#endif /* filesys/fsutil.h */
