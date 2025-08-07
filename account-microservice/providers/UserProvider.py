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


class UserProvider(object):

	def __init__(self):
		"""
		Create the connection with mongoDB
		"""
		self.myclient = pymongo.MongoClient(f"mongodb://{os.environ.get('MONGO_URL', 'localhost')}:{os.environ.get('MONGO_PORT', 27017)}/")
		self.mydb = self.myclient["steam"]
		self.mycol = self.mydb["user"]

	def create_user(self, steamUser):
		self.mycol.insert_one(steamUser)
		return json.loads(JSONEncoder().encode(steamUser)), 201


	def update_user(self, updateUser):
		# if self.mycol.count.documents({'_id': updateUser['_id']}, limit=1) != 0: 
		#     print("Found a user in DB with this id")
		user_query = {"_id": updateUser['_id']}
		new_values = {"$set": updateUser}

		x = self.mycol.update_one(user_query, new_values)
		if x.modified_count != 0:
			return {"message": "Success"}, 201
		else:
			return {"error": "user not modified"}, 403
		# else:
		#     # user not found
		#     return {"error": "user not found"}, 409