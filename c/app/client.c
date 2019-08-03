#include "global.h"

void start_client(){
    int                 sockfd;
    ssize_t             n;
    char                sendline[MAXLINE+1] ,recvline[MAXLINE+1];
    struct sockaddr_in  servaddr;
    // socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    bzero(&servaddr,sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(13);
    inet_pton(AF_INET,"127.0.0.1",&servaddr.sin_addr);
    // connect
    connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
    
    while( fgets(sendline,MAXLINE,stdin) != NULL ){
        write(sockfd,sendline,strlen(sendline));
        bzero(&recvline,sizeof(recvline));
        if( (n = read(sockfd,recvline,MAXLINE) ) > 0 ){
            recvline[n] = 0 ;
            printf("receive message from server. message = %s",recvline);
            // fputs(recvline,stdout);
        }
        bzero(&sendline,sizeof(sendline));
    }
    close(sockfd);
    exit(0);
}

