import sys, json, requests
from pymongo import MongoClient

def create_tenants():
	print ("Inside create_tenants")
	print "-------------------------"

	p = 1
	# tags = []

	db=MongoClient("192.168.4.78").bee_hive

	local_db = MongoClient("localhost").bee_hive.setup_details
	
	data = db.setup_details.find({"active":1})

	for d in data:
		tags = []
		temp_tenants = []
		tags = [d["env"], d["product"], d["ip"]]
		if "tenants" in d["details"] :
			for k in d["details"]["tenants"].keys():
				tmp = d["details"]["tenants"][k]["customer_name"]
				
				if ".com" not in tmp and ":" not in tmp :
					 temp_tenants.append(d["details"]["tenants"][k]["customer_name"].strip())


		tags = tags + temp_tenants
		print list(set(tags))
		d["tags"] = tags
		local_db.insert(d)

					



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
	# 				# print "-------------------------"
	# 				# tenants.append("{0} : {1} : {2} : {3}".format(d['details']['tenants'], d['product'], d['ip'], d['env']))
	# 				# print d['details']['tenants']
	# 				# print d
	# 				# print "-------------------------"
	# 			# p = p+1
	# # for t in tags:
	# # 	print t
	# my_set = sorted(set(tags))
	# return list(my_set)
	# print "Total = " +str(p)

def create_new_docs(db):
	print ("Inside create_new_docs")
	print "-------------------------"
	log_path = ""
	start_command = ""
	grep_path = ""
	stop_command = ""
	jdk_path = ""
	chmod_path = ""
	log_file = ""
	database_host = ""
	customer_name = ""
	product = ""
	env = ""
	ip = ""
	jboss_path = ""
	app_server = ""
	database_type = ""
	c = 1
	doc = 1

	# for item in tags:
	# 	# print item
	# 	c = c+1
	# print "	TOTAL searchable tags = " + str(c)
	# tags
	# db.newTags.insert(tags)
	data = db.swarmData.find({"active":1})

	for d in data:
		product = d['product']
		env = d['env']
		ip = d['ip']
		jboss_path = d['jboss_path']

		if 'log_path' in d['details']['setup_details'].keys():
			log_path = d['details']['setup_details']['log_path']
		else:
			log_path = "-"
		if 'start_command' in d['details']['setup_details'].keys():
			start_command = d['details']['setup_details']['start_command']
		else:
			start_command = "-"
		if 'app_server' in d['details']['setup_details'].keys():
			app_server = d['details']['setup_details']['app_server']
		else:
			app_server = "-"
		if 'grep_path' in d['details']['setup_details'].keys():
			grep_path = d['details']['setup_details']['grep_path']
		else:
			grep_path = "-"
		if 'stop_command' in d['details']['setup_details'].keys():
			stop_command = d['details']['setup_details']['stop_command']
		else:
			stop_command = "-"
		if 'jdk_path' in d['details']['setup_details'].keys():
			jdk_path = d['details']['setup_details']['jdk_path']
		else:
			jdk_path = "-"
		if 'database_type' in d['details']['setup_details'].keys():
			database_type = d['details']['setup_details']['database_type']
		else:
			jdk_path = "-"
		if 'chmod_path' in d['details']['setup_details'].keys():
			chmod_path = d['details']['setup_details']['chmod_path']
		else:
			chmod_path = "-"
		if 'log_file' in d['details']['setup_details'].keys():
			log_file = d['details']['setup_details']['log_file']
		else:
			log_file = "-"
		if 'database_host' in d['details']['setup_details'].keys():
			database_host = d['details']['setup_details']['database_host']
		else:
			database_host = "-"
		if 'details' in d.keys():
			if 'tenants' in d['details'].keys() and isinstance(d['details'], dict):
				if isinstance(d['details']['tenants'], dict):
					for key in d['details']['tenants'].keys():
						customer_name = d['details']['tenants'][key]['customer_name']
						
				else:
					customer_name = d['details']['tenants']
		db.newDocs.insert(
					{
						"product" : product,
						"ip" : ip,
						"tags" : [product, ip, env, customer_name],
						"details" : {
							"setup_details" : {
								"log_path" : log_path,
								"start_command" : start_command,
								"app_server" : app_server,
								"grep_path" : grep_path,
								"stop_command" : stop_command,
								"jdk_path" : jdk_path,
								"database_type" : database_type,
								"chmod_path" : chmod_path,
								"log_file" : log_file,
								"database_host" : database_host
								}
							},
						"customer_name" : customer_name,
						"env" : env,
						"jboss_path" : jboss_path

					}
					)
		doc = doc + 1
	print "Total docs added = " + str(doc)


		# customer_name = item.split(":")[0].strip()
		# product = item.split(":")[1].strip()
		# ip = item.split(":")[2].strip()
		# env = item.split(":")[3].strip()
		# data = db.swarmData.find({"active":1})
		# c = c+1
	# print "Total = " +str(c)  
		# print customer_name + " : " + product+ " : "+ ip+ " : " + env
		# doc = 1
		# for d in data:
		# 	if(d['product']==product and d['ip']==ip and d['env']==env):
		# 		# print d
		# 		if 'log_path' in d['details']['setup_details'].keys():
		# 			log_path = d['details']['setup_details']['log_path']
		# 		if 'start_command' in d['details']['setup_details'].keys():
		# 			start_command = d['details']['setup_details']['start_command']
		# 		if 'grep_path' in d['details']['setup_details'].keys():
		# 			grep_path = d['details']['setup_details']['grep_path']
		# 		if 'stop_command' in d['details']['setup_details'].keys():
		# 			stop_command = d['details']['setup_details']['stop_command']
		# 		if 'jdk_path' in d['details']['setup_details'].keys():
		# 			jdk_path = d['details']['setup_details']['jdk_path']
		# 		if 'chmod_path' in d['details']['setup_details'].keys():
		# 			chmod_path = d['details']['setup_details']['chmod_path']
		# 		if 'log_file' in d['details']['setup_details'].keys():
		# 			log_file = d['details']['setup_details']['log_file']
		# 		if 'database_host' in d['details']['setup_details'].keys():
		# 			database_host = d['details']['setup_details']['database_host']
		# 		db.newDocs.insert(
		# 			{
		# 				"product" : d[product],
		# 				"ip" : d[ip],
		# 				"tags" : [d[product], d[ip], d[env], customer_name],
		# 				"details" : {
		# 					"setup_details" : {
		# 						"log_path" : log_path,
		# 						"start_command" : start_command,
		# 						"grep_path" : grep_path,
		# 						"stop_command" : stop_command,
		# 						"jdk_path" : jdk_path,
		# 						"chmod_path" : chmod_path,
		# 						"log_file" : log_file,
		# 						"database_host" : database_host
		# 						}
		# 					},
		# 				"customer_name" : customer_name,
		# 				"env" : env

		# 			}
		# 			)
		# 		print "Doc no " +str(doc) + "for tenant no " +str(c)
		# 		print "-------------------------"
		# 		doc = doc+1
		# 	c = c+1
		

if __name__ == "__main__":
	# client = MongoClient('192.168.4.78',27017)
	# db = client.TURBATIO_SEARCH
	# data = db.swarmData.find({"active":1})
	# tags = create_tenants(data)
	# create_new_docs()
	create_tenants()
