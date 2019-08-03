//
//  global.h
//  c
//
//  Created by Junjie Zou on 2019/7/31.
//  Copyright © 2019 Junjie Zou. All rights reserved.
//

#ifndef global_h
#define global_h

#include <stdio.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// 错误处理有关的头文件
#include <errno.h>
#include <stdarg.h>        /* ANSI C header file */
#include <syslog.h>        /* for syslog() */

#define MAXLINE     4096
#define LISTENQ     1024

// socket 包裹函数
int     Socket(int, int, int);

// ** error 错误处理函数列表
void    err_sys(const char *, ...);

// app
void    start_client(void);
void    start_server(void);

#endif /* global_h */


/*
 编译脚本
 gcc -I ./ -c app/server.c -o app/server.o
 gcc -I ./ -c app/client.c -o app/client.o
 gcc -I ./ -c lib/wraper.c -o lib/wraper.o
 gcc -I ./ -c lib/error.c -o lib/error.o
 gcc -I ./ -c main.c -o main.o
 gcc -o main app/server.o app/client.o lib/wraper.o lib/error.o main.o
 */
