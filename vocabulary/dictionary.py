import requests
import xmltodict
import json

def iciba( w ):
	url = "http://dict-co.iciba.com/api/dictionary.php"
	key = "0A3831EC056EB0C7E685806578A63EC2"
	r = requests.get(url,params={'w':w , 'key':key})
	return json.dumps(xmltodict.parse(r.content))