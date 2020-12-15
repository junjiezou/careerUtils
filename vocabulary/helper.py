# 讲数据库查询出来的数据进行迭代，获取某个字段的所有值，放到元组里
def getFieldFromDictArray(srcDictArray , field):
	values = []
	for item in srcDictArray:
		values.append(item[field])
	return values

