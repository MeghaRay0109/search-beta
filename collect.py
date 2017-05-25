import sys, json, requests
from pymongo import MongoClient

def fetch_data(url):
	content = requests.get(url).text
	data = json.loads(content)
	return data

def add_to_mongo(data, client):
	print "add_to_mongo"
 	db = client.TURBATIO_SEARCH
 	for item in data:
		del(item["_id"])
 		result = db.swarmData.insert(item)
 	print "add_to_mongo completed"

def add_newdata_mongo(data_new, client):
	print "entered newdata"
 	db = client.TURBATIO_SEARCH
 	db.nodeTags.insert(data_new)
 	print "add_newdata_mongo completed"

if __name__ == "__main__":
	client = MongoClient('192.168.4.78',27017)
	url="http://turbatio.go.zycus.com/api/swarm/1/setups"
	tag_url = "http://turbatio.go.zycus.com/get_node_tags"
	data = fetch_data(url)
	data_new = fetch_data(tag_url)
	add_to_mongo(data, client)
	add_newdata_mongo(data_new, client)

	#tags = process_data(data)
	#for item in tags: 
	#print(item)
	