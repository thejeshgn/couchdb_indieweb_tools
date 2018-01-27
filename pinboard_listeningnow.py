# This is for daily import after the inital hug import
# I dont think there will be more than 1000 per day.
# You can make this script efficient
# Thejesh GN

import couchdb
import requests


couchdb_username="" 
couchdb_password="" 
couchdb_url=""
couchdb_db_name="listeningnow"

pinboard_token ="auth_token="
pinboard_url="https://api.pinboard.in/v1/posts/all"

update = True
check_for_update = True
one_page_count = 100
end_now = False

db_full_url = "https://"+couchdb_username+":"+couchdb_password+"@"+couchdb_url

couch = couchdb.Server(db_full_url)
database = couch[couchdb_db_name]

start = 0
while(not end_now):
	params = "?"+pinboard_token+"&"+"tag=listeningnow&meta=yes&format=json&results={0}&start={1}".format(one_page_count, start)
	URL = pinboard_url+params
	print URL
	#a = input("Press Enter to continue...")
	r = requests.get(URL)
	if r.status_code == 200:
		start = start + one_page_count
		response_json = r.json()
		posts = response_json
		for post in posts:
			print str(post)
			_id = post['hash'] #its a has of URL, so unique
			print _id
			tagstring = post['tags']
			tags = tagstring.split(" ")
			post['tags'] = tags
			if len(tags) > 2:
				print "-------------------- tags -------------------"
				print str(tags)
				for tag in tags:
					if tag.startswith("len="):
						l = tag.replace("len=","")
						post["period"] = int(l)
					if tag.startswith("pod="):
						pod = tag.replace("pod=","")
						post["podcast"] = pod
			try:
				if database[_id]:
					if update:
						existing_doc = database[_id]
						if check_for_update and existing_doc['meta'] == post['meta']:
							pass
						else:
							#Update update
							print "update"
							post['_id'] = _id
							post['_rev'] = existing_doc['_rev']
							del post['hash']
							database.save(post)
							print str(post)							
					else:
						#update is not required. else end the loop
						end_now = True
						break

			except couchdb.http.ResourceNotFound:
				print "insert"
				post['_id'] = _id
				del post['hash']
				database.save(post)
				print str(post)
	else:
		break






