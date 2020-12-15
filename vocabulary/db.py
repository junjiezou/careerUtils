import pymysql.cursors
import time,datetime
from DBUtils.PooledDB import PooledDB

# Connect to the database
# connection = pymysql.connect(host='111.230.15.197',user='vocabulary',password='v@2018ocA',db='vocabulary',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
# db_pool = PooledDB(pymysql,5,host='111.230.15.197',user='vocabulary',passwd='v@2018ocA',db='vocabulary',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
db_pool = PooledDB(pymysql,5,host='111.230.15.197',user='vocabulary',passwd='v@2018ocA',db='vocabulary',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

def makeInCondiction( field , tupleValues):
	tempArray = []
	for item in tupleValues:
		tempArray.append("%s")
	return "{} in ({})".format(field,",".join(tempArray))

# 查询words中有多少单词是在熟词中
def wordsInFamiliar( accountId , words ):
	connection = db_pool.connection()
	with connection.cursor() as cursor:
		sql = "select Word from voFamiliar where AccountId = %s and "+makeInCondiction("Word",words)
		print(sql)
		cursor.execute(sql, (accountId,) + words )
		result = cursor.fetchall()
		cursor.close()
		connection.close()
		return result

def wordsInStrange( accountId , words ):
	connection = db_pool.connection()
	with connection.cursor() as cursor:
		sql = "select Word from voStrange where AccountId = %s and "+makeInCondiction("Word",words) 
		cursor.execute(sql, (accountId,) + words )
		result = cursor.fetchall()
		cursor.close()
		connection.close()
		return result

# 批量导入生词: 先删除再批量insert，最后commit
def insertStrangeWords(accountId , words , source):
	connection = db_pool.connection()
	with connection.cursor() as cursor:
		sql = "delete from voStrange where AccountId = %s and " + makeInCondiction("Word",words) 
		cursor.execute(sql,(accountId,) + words )
		for word in words:
			sql = "INSERT INTO `voStrange` (`AccountId`, `Word`,Source,UpdateDate) VALUES (%s, %s, %s , %s )"
			cursor.execute(sql, (accountId , word , source, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) )
	connection.commit()
	connection.close()
	return True


def insertFamiliarWords( accountId , words , source ):
	try:
		connection = db_pool.connection()
		with connection.cursor() as cursor:
			sql = "delete from voStrange where AccountId = %s and " + makeInCondiction("word",words) 
			cursor.execute(sql,(accountId,) + words )

			for word in words:
				sql = "INSERT INTO `voFamiliar` (`AccountId`, `Word`,Source) VALUES (%s, %s, %s )"
				cursor.execute(sql, (accountId , word , source))

		connection.commit()
		connection.close()
	except:
		return False
	return True

def getStrangeWord( accountId ):
	connection = db_pool.connection()
	with connection.cursor() as cursor:
		sql = "select Word from voStrange where AccountId = %s order by UpdateDate asc , Word desc limit 1 "
		cursor.execute(sql, (accountId,) )
		result = cursor.fetchone()
		cursor.close()
		connection.close()
		return result

def switchStrangeToFamiliar( accountId , words ,source):
	try:
		connection = db_pool.connection()
		with connection.cursor() as cursor:
			sql = "delete from voStrange where AccountId = %s and " + makeInCondiction("word",words) 
			cursor.execute(sql,(accountId,) + words )

			for word in words:
				sql = "INSERT INTO `voFamiliar` (`AccountId`, `Word`,Source) VALUES (%s, %s, %s )"
				cursor.execute( sql, (accountId , word , '-' ) )
		connection.commit()
		connection.close()
	except:
		return False
	return True	

def markNextStrange(accountId , word ,d ):
	# try:
	connection = db_pool.connection()
	now = datetime.datetime.now()
	delta = datetime.timedelta(days=3)
	n_days = now + delta
	updatedate = n_days.strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "update voStrange set UpdateDate = %s where AccountId = %s and word = %s " 
		cursor.execute(sql,(updatedate,accountId,word))
	connection.commit()
	connection.close()
	# except:
	# 	return False
	# return True

"""
查询熟词库和生词库的总数
"""
def getSumarry(accountId):
	connection = db_pool.connection()
	with connection.cursor() as cursor:
			sql = "select count(1) as stranges from voStrange where AccountId = %s " 
			cursor.execute(sql,(accountId,))
			result = cursor.fetchone()
			stranges = result['stranges']
			
			sql = "select count(1) as familiars from voFamiliar where AccountId = %s " 
			cursor.execute(sql,(accountId,))
			result = cursor.fetchone()
			familiars = result['familiars']

			cursor.close()
			connection.close()
			return {"familiars":familiars,"stranges":stranges}

# try:
	# with connection.cursor() as cursor:
	# 	sql = "INSERT INTO `voAccount` (`AccountId`, `OpenId`,CommonId,Phone,CreateDate) VALUES (%s, %s,%s, %s,%s)"
	# 	cursor.execute(sql, ('AccountId', 'very-secret','AccountId', 'very-secret',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) )
	# connection.commit()

# 	with connection.cursor() as cursor:
# 		sql = "SELECT * FROM voAccount WHERE AccountId=%s"
# 		cursor.execute(sql, ('AccountId'))
# 		result = cursor.fetchall()
# 		# print(result)

# finally:
# 	connection.close()

