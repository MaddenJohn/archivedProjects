/* Prints the command-line arguments.
   This program is used for all of the args-* tests.  Grading is
   done differently for each of the args-* tests based on the
   output. */

#include "tests/lib.h"

int
main (int argc, char *argv[]) 
{
  int i;

 // test_name = "args";

  printf ("begin");
  printf ("argc = %d", argc);
  for (i = 0; i <= argc; i++)
	//printf ("ADDRESSS %p",  &argv[i]);
    if (argv[i] != NULL)
      printf ("argv[%d] = '%s'", i, argv[i]);
    else
      printf ("argv[%d] = null", i);
  printf ("end");

  return 0;
}
