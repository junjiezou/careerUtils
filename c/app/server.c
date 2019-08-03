#include "global.h"

void start_server(){
    int                 listenfd,connfd;
    ssize_t             n;
    char                buff[MAXLINE+1];
    struct sockaddr_in  servaddr;
    // socket
    listenfd = Socket(AF_INET, SOCK_STREAM, 0); // 1、替换为包裹函数
    bzero(&servaddr,sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(13);
    // bind
    bind(listenfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
    // listen
    listen(listenfd,LISTENQ);
    for(;;){
        connfd = accept(listenfd,NULL,NULL);
        while( ( n = read(connfd,buff,MAXLINE)) > 0 ){
            printf("receive message from client. message = %s",buff);
            write(connfd,buff,strlen(buff));
            bzero(&buff,sizeof(buff));
        }
        close(connfd);
    }
}
