# This is for daily import after the inital hug import
# I dont think there will be more than 1000 per day.
# You can make this script efficient
# Thejesh GN

import couchdb
import requests


couchdb_username="" 
couchdb_password="" 
couchdb_url=""
couchdb_db_name="bookmarks"

pinboard_username=""
pinboard_password=""
pinboard_url="api.pinboard.in/v1/posts/all"

update = False
one_page_count = 100

db_full_url = "https://"+couchdb_username+":"+couchdb_password+"@"+couchdb_url
pinboard_url = "https://"+pinboard_username+":"+pinboard_password+"@"+pinboard_url
couch = couchdb.Server(db_full_url)
database = couch[couchdb_db_name]


while(True):
	start = 0
	params = "?format=json&results={0}&start={1}".format(one_page_count, start)
	r = requests.get(pinboard_url+params)
	if r.status_code == 200:
		start = start + one_page_count
		response_json = r.json()
		posts = response_json
		for post in posts:
			_id = post['hash']
			print _id
			try:
				if database[_id]:
					if update:
						existing_doc = database[_id]
						if existing_doc['meta'] == post['meta']:
							pass
						else:
							#Update update
							print "update"
							post['_id'] = _id
							post['_rev'] = existing_doc['_rev']
							del post['hash']
							database.save(post)
							print str(post)
							break;
			except couchdb.http.ResourceNotFound:
				print "insert"
				post['_id'] = _id
				del post['hash']
				database.save(post)
	else:
		break






