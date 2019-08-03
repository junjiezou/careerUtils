#include "global.h"

int main(int argc, const char * argv[]){
    if(strcmp(argv[1],"start_server") == 0){
        start_server();
    }
    if(strcmp(argv[1],"start_client") == 0){
        start_client();
    }
}
