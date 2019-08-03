//
//  wraper.c
//  c
//
//  Created by Junjie Zou on 2019/7/31.
//  Copyright © 2019 Junjie Zou. All rights reserved.
//

#include "global.h"

// 2、socket包裹函数，命名为Socket，方便区分使用
int Socket(int family, int type, int protocol){
    int n;
    if ( (n = socket(family, type, protocol)) < 0)
        err_sys("socket error");
    return(n);
}

