import re,json,urllib,hashlib
from flask import Flask,request,abort, redirect, url_for,session,escape,make_response,render_template
import dictionary , parseWebPage, validators , db,helper

app = Flask(__name__)

"""
todo 还得看看flask里面怎么做权限控制
登录账号为手机号码，密码需要insert到数据库
"""

"""
1、查询出熟词表的个数，点击浏览，则进入一个分页tab，分页展示熟词。todo 后面再补这个功能
2、生词表的个数，点击开始复习按钮则进入生词复习功能
3、已掌握词汇：中学、高中、大学四级、专业四级、专业八级、雅思 等等
"""
@app.route('/')
def index():
	sumarry = db.getSumarry('junjiezou')
	return render_template('index.html', name="Jackiezou !",sumarry=sumarry)

"""
翻译接口，金山词霸
"""
@app.route('/iciba/<w>')
def iciba( w ):
	if( re.match(r'\w+', w , re.I) == None ) :
		return json.dumps({'success': False}) 
		# 字符不合法试，返回空
	if( w.isupper() == False ):
		w = w.lower()
	translate = json.loads( dictionary.iciba(w) )
	# return str(translate)
	translate = translate['dict'];
	return json.dumps({'success': True,'translate': translate}) #返回字典查询结果

"""
解释URL
1、获取本页面所有单词，跟本人熟词库做匹对，不在熟词库中的词都入库到生词库
2、遍历当前页面中所有a标签，发起请求并获取相应链接的页面
	递归所有页面，并获取所有页面的单词，以步骤一做匹对写入生词库
3、把分析结果写入文件
返回汇总信息
{
	success: True | False
	url:"http:*****"
	familiar:123
	strange:321
	batchId:
}
用户可以在页面上直接点击全部添加到生词库
只支持非登录态的网页
"""
@app.route('/parseUrl')
def parseUrl( ):
	url = request.args.get('url')
	# url = 'https://github.com/'
	if( validators.isurl(url) == False ):
		return json.dumps( { 'success': False,'message':'Bad url!' } )
	result = parseWebPage.parseUrl(url)
	familiarWords = db.wordsInFamiliar('junjiezou',tuple(result))
	familiarWords = helper.getFieldFromDictArray(familiarWords,'Word')
	strangeWords = db.wordsInStrange('junjiezou',tuple(result))
	strangeWords = helper.getFieldFromDictArray(strangeWords,'Word')
	unknowWords = set(result) - set(familiarWords) - set(strangeWords)
	content = {	'result':tuple(result),
	'familiarWords':tuple(familiarWords),
	'strangeWords':tuple(strangeWords),
	'unknowWords':tuple(unknowWords),
	'familiar': len(familiarWords),
	'strange':len(strangeWords),
	'unknow':len(unknowWords),
	'url':url,
	}
	contentString = str(content)
	md5 = hashlib.md5()
	md5.update(contentString.encode("utf-8"))
	content['batchId'] = md5.hexdigest()
	with open("./temporaryFile/"+content['batchId'],"w") as file:
		file.write(json.dumps(content))
	return json.dumps({'success':True,'url':url,'familiar':content['familiar'],'strange':content['strange'],'unknow':content['unknow'],'batchId':content['batchId']})


"""
解释句子
"""
@app.route('/parseSentence')
def parseSentence( ):
	sentence = request.args.get('sentence')
	pattern = re.compile(r'[a-zA-Z]{3,}')
	result = pattern.findall(sentence)
	familiarWords = db.wordsInFamiliar('junjiezou',tuple(result))
	familiarWords = helper.getFieldFromDictArray(familiarWords,'Word')
	strangeWords = db.wordsInStrange('junjiezou',tuple(result))
	strangeWords = helper.getFieldFromDictArray(strangeWords,'Word')
	unknowWords = set(result) - set(familiarWords) - set(strangeWords)
	content = {	'result':tuple(result),
	'familiarWords':tuple(familiarWords),
	'strangeWords':tuple(strangeWords),
	'unknowWords':tuple(unknowWords),
	'familiar': len(familiarWords),
	'strange':len(strangeWords),
	'unknow':len(unknowWords),
	'sentence':sentence,
	}
	contentString = str(content)
	md5 = hashlib.md5()
	md5.update(contentString.encode("utf-8"))
	content['batchId'] = md5.hexdigest()
	with open("./temporaryFile/" + content['batchId'], "w") as file:
		file.write(json.dumps(content))
	return json.dumps({'success':True,'sentence':sentence,'familiar':content['familiar'],'strange':content['strange'],'unknow':content['unknow'],'batchId':content['batchId']})


"""
parseurl 会生成batchId,把整个批次的单词都导入到生词库

"""
@app.route('/batchMarkStrange/<batchId>')
def batchMarkStrange(batchId):
	with open("./temporaryFile/"+batchId,"r") as file:
		result = file.readline()
		result = json.loads(result)
		unknowWords = result['unknowWords']
		if( db.insertStrangeWords('junjiezou', tuple(unknowWords) ,"batchMarkStrange_"+batchId ) == True ):
			return json.dumps( { 'success': True,'message':'Mark !' } )
	return json.dumps( { 'success': False,'message':'Oh shit !' } )

"""
获取一个生词
在数据库中会有用户的生词列表，搜索列表中的生词，获取一个并把生词状态标记上
"""
@app.route('/strange')
@app.route('/strange/<w>/<d>')
def strange(w = False,d = False):
	if( w and d != False ):
		db.markNextStrange('junjiezou', w , d )
	word = db.getStrangeWord('junjiezou')
	if(word != False):
		return json.dumps( { 'success': True, 'word':word } )
	return json.dumps( { 'success': False } )

"""
把一个单词标记为生词，如果单词在熟词库则标记为删除状态
然后insert 到生词库
"""
@app.route('/markStrange/<w>')
def markStrange(w):
	if(db.insertStrangeWords('junjiezou', (w,) ,"markStrange") == True):
		return json.dumps( { 'success': True } )
	return json.dumps( { 'success': False } )

"""
把一个单词标记为熟词
然后insert 到熟词库，并删除生词库
"""
@app.route('/markFamiliar/<w>')
def markFamiliar(w):
	if(db.insertFamiliarWords('junjiezou', (w,) ,"markFamiliar") == True ):
		return json.dumps( { 'success': True } )
	return json.dumps( { 'success': False } )
