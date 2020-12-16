import requests
from html.parser import HTMLParser
import re,validators

"""
20190117 添加逻辑，把句子查出来，然后查询句子中的生词，如果是生词则把句子保存为单词的例句。
找句子的过程
1、从 p h1 h2 h3 h4 h5 div a 标签上获取句子。
2、过滤句子中的特殊标签。特殊标签要留一个数组列表，方便添加
3、对逐个句子生成hashkey 然后upsert进数据库
4、然后获取句子中的单词，塞入一个集合，进行下一步。

"""
def parseUrl( url ):
	try:
		r = requests.get(url)
		parser = MyHTMLParser()
		parser.words = set()
		parser.feed( r.text )
		words = parser.words
		# 以下代码是可以正常运作的，但是要把这块逻辑去掉，因为查询太久
		# 而且一次性带出的新词汇太多，有碍用户体验并且给用户带来太多生词，比较容易气馁
		for x in parser.hrefs:
			try:
				r = requests.get(x,timeout=1)
				text = r.text
			except:
				text = ''
			singleParse = SinglePageParse()
			singleParse.feed( text )
			words.update(singleParse.words)
		return words
	except:
		return ('apple','egg','word') # 测试数据

class MyHTMLParser(HTMLParser):
	hrefs = set() #存储a链接
	words = set()	#存储解释出来的单词
	currentTag = ''
	def handle_starttag(self, tag, attrs):
		self.currentTag = tag
		if( tag == 'a'):
			for name,value in attrs:
				if ( name == 'href' and validators.isurl(value) ) :
					self.hrefs.add(value)
					break
				
	def handle_data(self, data):
	# 匹配所有的英文句子
		if( self.currentTag.lower() in ['div'] ): # ,'h1','h2','h3','h4','h5','div','a','code','li','dl','span'
			if('' == data.strip() ):
				return
			print('SRC DATA::: '+data);
			print(re.match( r'^[a-z0-1A-Z\. \'",\?\!\:<>\-\(\)\\n]+$', data, re.M|re.I));
			if(None ==  re.match( r'^[a-z0-1A-Z\. \'",\?\!\:<>\-\(\)\\n]+$', data, re.M|re.I)):
				return
			print('TEST TRUE::: ');
			print(self.currentTag);
			print(data);
			pattern = re.compile(r'[a-zA-Z]')
			tempWords = pattern.findall(data)
			
			temp = []
			for word in tempWords:
				if( word.isupper() == False ):
					temp.append( word.lower() )
				else:
					temp.append(word)
			self.words.update(temp)

class SinglePageParse(HTMLParser):
	words = set()
	currentTag = ''
	def handle_starttag(self, tag, attrs):
		self.currentTag = tag
				
	def handle_data(self, data):
	# 匹配所有的英文单词
		if( self.currentTag not in ['script','style','link','img'] ):
			pattern = re.compile(r'[a-zA-Z]{3,}')
			tempWords = pattern.findall(data)
			self.words.update(tempWords)