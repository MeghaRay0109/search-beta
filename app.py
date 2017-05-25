from flask import Flask, render_template, request
import logging
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
import requests
import json
from bson.json_util import dumps
import collections

app = Flask(__name__, static_folder="static")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/api/search", methods=["GET"])
def search_api():
    if request.method == "GET":
        obj = requests.get("http://turbatio.go.zycus.com/api/swarm/1/setups").text
        return obj
    return "Error"

@app.route("/api/tags", methods=["GET"])
# def tags_api():
# 	client = MongoClient('localhost',27017)
#  	db = client.TURBATIO_SEARCH
#  	data = db.swarmData.find()
#  	search_tags = []
# 	for item in data:
# 		search_tags.append(item.get("product") + ": Product")
# 		search_tags.append(item.get("env") + ": Environment")
# 		search_tags.append(item.get("ip") + ": IP")
# 	search_set = set(search_tags)
# 	return json.dumps(list(search_set))
def create_tags():
	local_db = MongoClient("localhost").bee_hive.setup_details
	data = local_db.find({"active":1})
	tags = []
	for d in data:
		for t in d['tags']:
			tags.append(t)


	# *************************************************
	# client = MongoClient('192.168.4.78',27017)
	# db = client.TURBATIO_SEARCH
	# data = db.swarmData.find({"active":1})
	# tags = []
	# for d in data:
	# 	if 'details' in d.keys():
	# 		if 'tenants' in d['details'].keys() and isinstance(d['details'], dict):
	# 			if isinstance(d['details']['tenants'], dict):
	# 				for key in d['details']['tenants'].keys():
	# 					tags.append(d['product'])
	# 					tags.append(d['ip'])
	# 					tags.append(d['details']['tenants'][key]['customer_name'])
	# 					tags.append(d['env'])
	# 					# tenants.append("{0} : {1} : {2} : {3}".format(d['details']['tenants'][key]['customer_name'], d['product'], d['ip'], d['env']))
	# 					# print d['details']['tenants'][key]['customer_name'] + " : " + d['product'] + " : " + d['ip'] + " : " + d['env']
	# 			else:
	# 				tags.append(d['product'])
	# 				tags.append(d['ip'])
	# 				tags.append(d['details']['tenants'])
	# 				tags.append(d['env'])
	# **************************************************

	#mongo json map

	# search_map = {"env" : "Environment", "product" : "Product", "ip" : "IP"}

	# client = MongoClient('192.168.4.78',27017)
 # 	db = client.TURBATIO_SEARCH
 # 	mongo_data = db.swarmData.find()
 # 	node_tags = db.nodeTags.find()
	# tags = []

	# for d in mongo_data:
	# 	for k,v in search_map.iteritems():
	# 		# Production
	# 		first_tag = d[k]
	# 		# Environment
	# 		second_tag = v
	# 		tags.append("{0} : {1}".format(first_tag, second_tag))	# ["production : Environment"]

	# for cust in node_tags:
	# 	for tenant in cust["Tennant"]["customer_name"]:
	# 		label = "Customer"
	# 		tags.append("{0} : {1}".format(tenant, label))

	# for customer in node_tags["Tennant"]["customer_name"]:
	# 	label = "Customer"
	# 	tags.append("{0} : {1}".format(customer, label))

	my_set = sorted(set(tags))

	return json.dumps(list(my_set))


@app.route("/api/query", methods=["GET"])
def query_api():

	local_db = MongoClient("localhost").bee_hive.setup_details
 	# query_dict = dict(item.split(": ") for item in param.split(","))
 	# param = {"Demo : Environment", "10.40.3.9 : IP"}
 	# param = {"10.40.3.9 : IP"}
 	param = request.args.get('query').split(",")
 	app.logger.info(param)
 	# search_map = {"Environment" : "env", "Product" : "product", "IP" : "ip"}

	 #eg. {"tags":"10.40.3.8"}
	mongo_where_list = [] # list of mongo_where_dict dictionaries
	mongo_where = {} # pass this to find()
	for q in param:
		mongo_where_dict = {}
		mongo_where_dict["tags"] = q
		mongo_where_list.append(mongo_where_dict)

		#"production : Environment"
		# key = q.split(":")[0].strip()
		# value = q.split(":")[1].strip()

		# mongo_key = search_map[value]
		# mongo_value = key
		# mongo_where[mongo_key] = mongo_value
	mongo_where["$and"] = mongo_where_list
	app.logger.info(mongo_where)
	res = local_db.find(mongo_where)
	# return json.dumps(mongo_where)
	# json_data = json.dumps(dict([for r in res]))
	# return json_data
	results = []

	for r in res:
		results.append(r)
	# app.logger.info(dumps(results))
	flat_dict = []
	for item in results:
		if 'tenants' in item['details'].keys() :
			del item['details']['tenants']
		if 'start_seq_list' in item['details']['setup_details'].keys():
			del item['details']['setup_details']['start_seq_list']
		if 'stop_seq_list' in item['details']['setup_details'].keys():
			del item['details']['setup_details']['stop_seq_list']
		# app.logger.info(dumps(item))
		flat_dict.append(flatten(item))
	for d in flat_dict:
		del d['tags']
	return dumps(flat_dict)

def flatten(d, parent_key='', sep='#'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


@app.route("/search", methods = ["GET"])
def search():
    if request.method == "GET":
        return render_template("search2.html")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
