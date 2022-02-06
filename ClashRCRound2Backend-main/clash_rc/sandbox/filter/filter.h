#include<seccomp.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stddef.h>

void put_filter()
{
    scmp_filter_ctx f;
    f = seccomp_init(SCMP_ACT_KILL);

    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(ioctl), 0); //input output system call
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0); //terminates all threads
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0); //terminates calling threads
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);  //reads
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);  //close
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(sigreturn), 0);   //return from signal handler
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(sigaltstack), 0);    //set and/or get signal stack context
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);  //open
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);  //write to a file descriptor
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(fstat),0);   //obtains information about an open file
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(brk),0); //change size of data segment
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(lseek),0);   //changes the positions of the read/write pointer within the file
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(writev),0);  //read or write data into multiple buffers
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(execve), 0); //execute program
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(execveat), 0); //execute program relative to a directory file descriptor
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(mmap),0);    //map files or devices into memory
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(munmap),0);  //unmap files or devices into memory
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(mprotect), 0); //set protection on a region of memory
    seccomp_rule_add(f, SCMP_ACT_ALLOW, SCMP_SYS(access),0);  //determines whether the calling process has access permission to a file
    

    seccomp_load(f);
}