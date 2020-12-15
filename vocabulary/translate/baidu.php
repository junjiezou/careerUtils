<?php
/**
 * Created by PhpStorm.
 * User: jackiezou
 * Date: 2018/8/12
 * Time: 16:40
 */

$url = "http://api.fanyi.baidu.com/api/trans/vip/translate";

$q = '翻译为源语言';
$from = 'zh';
$to = 'en';

$appKey = '20180812000193635'; // app_id
$appSecret = 'QreWzNmclPanYxUW6jOP';
$salt = random_int(10000,99999);

$sign =md5( $appKey . $q . $salt .$appSecret  ) ;

$query = array('q'=>$q,'from'=>$from,'to'=>$to,'appid'=>$appKey,'salt'=>$salt,'sign'=>$sign);

$result = file_get_contents($url.'?'.http_build_query($query));

echo '<pre>'.print_r( json_decode($result,true),true).'<pre>';


// http://dict-co.iciba.com/api/dictionary.php?w=document&key=0A3831EC056EB0C7E685806578A63EC2

