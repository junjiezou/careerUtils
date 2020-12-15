<?php
/**
 * Created by PhpStorm.
 * User: jackiezou
 * Date: 2018/8/12
 * Time: 16:40
 */

$url = "http://openapi.youdao.com/api";

$q = '源语言';
$from = 'zh-CHS';
$to = 'EN';

$appKey = '048b33c326fe16c1'; // app_id
$appSecret = 'qBy3s0tufHhWOa6f1r5tAPQ8ZgW6nVJr';
$salt = random_int(10000,99999);

$sign =strtoupper( md5( $appKey . $q . $salt .$appSecret  ) );

$query = array('q'=>$q,'from'=>$from,'to'=>$to,'appKey'=>$appKey,'salt'=>$salt,'sign'=>$sign);

$result = file_get_contents($url.'?'.http_build_query($query));

echo '<pre>'.print_r( json_decode($result,true),true).'<pre>';