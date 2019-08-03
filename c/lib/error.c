//
//  error.c
//  c
//
//  Created by Junjie Zou on 2019/7/31.
//  Copyright © 2019 Junjie Zou. All rights reserved.
//

#include "global.h"

int daemon_proc; // 一个全局变量，用于控制应用日志是否输出到系统日志，本案例不使用系统日志，因此变量会保持为常量0.
// 4、打印错误日志
static void err_doit(int errnoflag, int level, const char *fmt, va_list ap){
    int     errno_save;
    long    n;
    char    buf[MAXLINE + 1];
    
    errno_save = errno; // 5、记录全局错误码
#ifdef    HAVE_VSNPRINTF
    vsnprintf(buf, MAXLINE, fmt, ap);/* safe */
#else
    vsprintf(buf, fmt, ap);/* not safe 按格式打印日志 */ // 本案例没有定义 HAVE_VSNPRINTF ，所以直接走这个函数
#endif
    n = strlen(buf);
    // 6、如果错误码存在，则获取错误码对应的描述
    if (errnoflag)
        snprintf(buf + n, MAXLINE - n, ": %s", strerror(errno_save));
    strcat(buf, "\n");
    
    if (daemon_proc) {
        syslog(level, buf);//打印日志到系统日志，系统日志默认是/var/log/messages，具体知识点使用的时候再翻资料
    } else {
        fflush(stdout);        /* in case stdout and stderr are the same */
        fputs(buf, stderr);
        fflush(stderr);
    }
    return;
}

//3、系统调用发生致命错误时,往控制台打印日志并退出系统。【Tips】fmt参数可以是一个带格式的字符串
void err_sys(const char *fmt, ...){
    va_list ap;
    va_start(ap, fmt); // 用省略号指定参数列表时，用va_start函数来获取参数列表中的参数，使用完毕后调用va_end()结束
    err_doit(1, LOG_ERR, fmt, ap);
    va_end(ap);
    exit(1); // 正常退出的代码是 0
}

