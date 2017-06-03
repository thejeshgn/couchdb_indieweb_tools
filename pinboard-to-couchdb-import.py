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
params = "?format=json&results=1000&start=0"

db_full_url = "https://"+couchdb_username+":"+couchdb_password+"@"+couchdb_url
pinboard_url = "https://"+pinboard_username+":"+pinboard_password+"@"+pinboard_url
couch = couchdb.Server(db_full_url)
database = couch[couchdb_db_name]
r = requests.get(pinboard_url+params)
if r.status_code == 200:
	response_json = r.json()
	posts = response_json
	for post in posts:
		_id = post['hash']
		print _id
		try:
			if database[_id]:
				print "Document with "+_id+" already exists."
		except couchdb.http.ResourceNotFound:
			post['_id'] = _id
			del post['hash']
			database.save(post)






