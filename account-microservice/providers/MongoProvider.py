import json
import os
import pymongo
from bson import ObjectId
from bson.json_util import dumps


class JSONEncoder(json.JSONEncoder):
	"""
	Extend JSON Encoder to support mongoDB id encoding
	"""
	def default(self, o):
		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self, o)


class MongoProvider(object):

	def __init__(self):
		"""
		Create the connection with mongoDB
		"""
		self.myclient = pymongo.MongoClient(f"mongodb://{os.environ.get('MONGO_URL', 'localhost')}:{os.environ.get('MONGO_PORT', 27017)}/")
		self.mydb = self.myclient["steam"]
		self.mycol = self.mydb["discountgame"]


	def read_game_by_title(self, gameTitle):
		
		print(f"Database: {self.mydb.name}")
		print(f"Collection:  {self.mycol.name}")
		collections = self.mydb.list_collection_names()
		print(f"Available collections: {collections}")
		count = self.mycol.count_documents({})
		print(f"Number of documents in collection: {count}")

		if self.mycol.count_documents({'title': gameTitle}, limit=1) != 0:
			user_query = {"title": gameTitle}

			user = self.mycol.find_one(user_query)
			# print(f"Found user: {user}")
			user = JSONEncoder().encode(user)
			return json.loads(user), 200
		else:
			return {"error": "user not found"}, 400

	def read_all_games(self):
		logs = self.mycol.find()
		logs_list = list(logs)
		print(logs_list)

		collections = self.mydb.list_collection_names()
		print(f"Available collections: {collections}")
		count = self.mycol.count_documents({})
		print(f"Number of documents in collection: {count}")
		
		# Use dumps and parse back to dict for consistent return format
		json_string = dumps(logs_list)
		logs_dict = json.loads(json_string)
		return {"logs": logs_dict}, 200
	


	# def update_user(self, payload):
		
	# 	if self.mycol.count_documents({'id': payload['id']}, limit=1) != 0: # Check if user exists in DB
	# 		print("Found a user in DB with this id")
	# 		user_query = {"id": payload['id']}
	# 		new_values = {"$set": payload}

	# 		x = self.mycol.update_one(user_query, new_values)
	# 		if x.modified_count != 0:
	# 			return {"message": "Success"}, 201
	# 		else:
	# 			return {"error": "user not modified"}, 403
	# 	else:
	# 		# user not found
	# 		return {"error": "user not found"}, 409

	# def delete_user(self, user_id):
		
	# 	user_query = {"id": user_id}
	# 	x = self.mycol.delete_one(user_query)
	# 	if x.deleted_count != 0:
	# 		return {"message": "Success"}, 200

	# 	else:
	# 		return {"error": "user not found"}, 400
