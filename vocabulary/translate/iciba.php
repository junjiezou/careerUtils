<?php
/**
 * Created by PhpStorm.
 * User: jackiezou
 * Date: 2018/8/12
 * Time: 16:40
 */

$url = "http://dict-co.iciba.com/api/dictionary.php";

$key = '0A3831EC056EB0C7E685806578A63EC2';
$w = $_GET['w'];
if(empty($w) || !is_string($w)) {
    echo 0;
    die();
}
$query = array('key'=>$key,'w'=>$w);
$resultXml = file_get_contents($url.'?'.http_build_query($query));

$result = xmlstr_to_array($resultXml);

echo json_encode($result);
die();

echo '<pre>'.print_r( $result,true).'<pre>';


// http://dict-co.iciba.com/api/dictionary.php?w=document&key=0A3831EC056EB0C7E685806578A63EC2

function xmlstr_to_array($xmlstr) {
    $doc = new DOMDocument();
    $doc->loadXML($xmlstr);
    $root = $doc->documentElement;
    $output = domnode_to_array($root);
    $output['@root'] = $root->tagName;
    return $output;
}
function domnode_to_array($node) {
    $output = array();
    switch ($node->nodeType) {
        case XML_CDATA_SECTION_NODE:
        case XML_TEXT_NODE:
            $output = trim($node->textContent);
            break;
        case XML_ELEMENT_NODE:
            for ($i=0, $m=$node->childNodes->length; $i<$m; $i++) {
                $child = $node->childNodes->item($i);
                $v = domnode_to_array($child);
                if(isset($child->tagName)) {
                    $t = $child->tagName;
                    if(!isset($output[$t])) {
                        $output[$t] = array();
                    }
                    $output[$t][] = $v;
                }
                elseif($v || $v === '0') {
                    $output = (string) $v;
                }
            }
            if($node->attributes->length && !is_array($output)) { //Has attributes but isn't an array
                $output = array('@content'=>$output); //Change output into an array.
            }
            if(is_array($output)) {
                if($node->attributes->length) {
                    $a = array();
                    foreach($node->attributes as $attrName => $attrNode) {
                        $a[$attrName] = (string) $attrNode->value;
                    }
                    $output['@attributes'] = $a;
                }
                foreach ($output as $t => $v) {
                    if(is_array($v) && count($v)==1 && $t!='@attributes') {
                        $output[$t] = $v[0];
                    }
                }
            }
            break;
    }
    return $output;
}

