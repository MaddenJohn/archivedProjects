With sema down
begin
load: no such file: open failed
no such file: exit(-1)
exec-missing: exit(-1)

without sema down
begin 
exec(no such file):4
end
exit(0)
load: no such file_open failed
no such file: exit(0) KERNAL PANIC











TESTS FAILING

main 6
exec-missing
rox-child
rox-multichild
multi-oom
syn-read
syn-write


tests failing for semaphore solution
wait-simple
wait-twice
multi-recurse
multi-child-fd

tests failing for check cmd line in syscall
exec-arg
multi-recurse
multi-child-fd