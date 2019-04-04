from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
#internal
import config as conf

# Load Logging definition
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('tornado-info')


class ManageDB():
    def __init__(self, collection_string):
        self.client = MongoClient(conf.MONGO_URI)
        self.db = self.client[conf.DEFAULT_DB]
        self.collection = self.db[collection_string]

    def set_collection(self, collection):
        self.collection = collection

    def get_collection(self):
        return self.collection

    def get_db(self):
        return self.db

    def close(self):
        self.client.close()

    def get_autoincrement_id(self, collectionName):
        id = 0
        result = []
        try:
            docs = self.collection.find({"collectionName": collectionName})
            if docs != None:
                result = list(docs)
                id = int(result[0].get("counter") + 1)
                self.collection.update_many(result[0], {"$set": {"counter": id}}, upsert=False)
            else:
                id = 0
                logger.info("no counter")
        except Exception as e:
            logger.info(e)

        return str(id)

    def delete(self, key, value):
        result = "Failed"
        resulting = self.collection.delete_many({key: value})
        deletedCount = resulting.deleted_count
        if deletedCount > 0:
            result = "Deleted"

        return result

    def delete_json(self, myjson):
        result = "Failed"
        resulting = self.collection.delete_many(myjson)
        deletedCount = resulting.deleted_count
        if deletedCount > 0:
            result = True
        return result

    def insert_json(self, myjson):
        result = "Failed"
        resulting = self.collection.insert_one(myjson).inserted_id
        if resulting is not None:
            result = True

        return result

    def upsert(self, key, value, myjson):
        result = []
        myjson.update({"editFlag": 1})
        jsonKey = {key: value}
        docs = self.collection.update_many(jsonKey, {"$set": myjson}, upsert=True)
        if docs is not None:
            result = list(docs)

        return result

    def upsert_json(self, keyjson, myjson):
        result = True
        docs = self.collection.update_many(keyjson, {"$set": myjson}, upsert=True)

        return result

    def update(self, jsonKey, myjson):
        result = []
        docs = self.collection.update_many(jsonKey, {"$set": myjson}, upsert=False)
        if docs is not None:
            result = True

        return result

    def select_by_id(self, value):
        result = []
        doc = self.collection.find({'_id': ObjectId(value)})
        if doc is not None:
            result = list(doc)
        return result

    def select(self, key, value):
        result = []
        docs = self.collection.find({key: value})
        if docs is not None:
            result = list(docs)
        return result

    def _select_json(self, json):
        result = []
        docs = self.collection.find(json)
        if docs is not None:
            result = list(docs)
        return result

    def select_json(self, json):
        result = []
        docs = self.collection.find(json, {'_id': False})
        if docs is not None:
            result = list(docs)
        return result

    def select_from_list(self, key, mylist):
        result = []
        docs = self.collection.find({key: {"$in": mylist}}, {'_id': False})
        if docs is not None:
            result = list(docs)
        return result

    def select_and(self, jsonlist):
        result = []
        docs = self.collection.find({"$and": jsonlist}, {'_id': False})
        if docs is not None:
            result = list(docs)
        return result

    def select_or(self, jsonlist):
        result = []
        docs = self.collection.find({"$or": jsonlist}, {'_id': False})
        if docs is not None:
            result = list(docs)
        return result
