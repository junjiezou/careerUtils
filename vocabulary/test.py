import requests,sys
from html.parser import HTMLParser
import re,validators,parseWebPage,hashlib


url = 'C:/Users/jackiezou/Desktop/home.html'
result = ''
file =  open(url,"r")
l = file.readline()
while ( l ):
	result = result + l
	l = file.readline()

"""
1、对URL做md5获取页面ID，用于标记数据来源
2、对页面内容进行处理，处理成只剩带标点符号的文本。
3、遍历每个句子，获取句子里面的单词，对生词和熟词进行分类存放。
	如果有生词，则对句子进行存放，为了区分重复的句子，也得对句子做md5
	如果没有生词就可以不存放
4、遍历存在生词的句子，查询句子的中文意思，用于页面参考（预留字段给用户进行修正）
"""
md5 = hashlib.md5()
md5.update(url.encode('utf-8'))
srcMd5 = md5.hexdigest()

result = re.sub(r'<style[^>]+>[^>]+>',' ',result)
result = re.sub(r'<style>[^>]+>',' ',result)
result = re.sub(r'(</li>)|(</h\d>)|(</dl>)|(</LI>)|(</H\d>)|(</DL>)','. ',result) # 这些标签代表句子的结尾
result = re.sub(r'<[^>]+>',' ',result)
result = re.sub(r'[^a-z0-1A-Z\. \'",\?\!\:<>\-\(\)\\n;\[\]]',' ',result) # 非构成句子的成分
result = re.sub(r'(gt;)|(nbsp;)|(lt;)|(\( \))','',result) # 多余的字符
result = re.sub(r' {2,}',' ',result)
matchs = re.finditer(r'[^\.\!\?\;]+[\.\!\?\;]',result)
sentences = {}
for it in matchs: 
    sentence = it.group()
    sentence = sentence.strip()
    if None==re.match( r'.+[a-z0-1A-Z]+.+', sentence, re.M|re.I):
    	continue
    md5.update(sentence.encode('utf-8'))
    sentenceMd5 = md5.hexdigest()
    sentences[sentenceMd5] = sentence

words = set()
familiarWords = set()
strangeWords = set()
for it in sentences.keys():
	print(it)
	print(sentences[it])

sys.exit()


# # parser = parseWebPage.MyHTMLParser()
# # parser.words = set()
# # parser.feed( result )
# words = parser.words
# print(words)

# batchId = "bc19a4b01bb3f3a65f5113d34beb4e08"
# with open("./temporaryFile/"+batchId,"r") as file:
# 		result = file.readline()
# 		result = json.loads(result)
# 		unknowWords = result['unknowWords']
# 		print(unknowWords)
# 		db.insertStrangeWords('junjiezou', tuple(unknowWords) ,"batchMarkStrange"+batchId )

