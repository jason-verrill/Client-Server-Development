from pymongo import MongoClient
from bson.json_util import dumps
import json

# CRUD interface for AAC.animals
class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    empty_exception = 'Nothing to save, because data parameter is empty'

    def __init__(self, username, password, port_number=54161):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        try:
            self.client = MongoClient('mongodb://%s:%s@localhost:%s' % (username, password, port_number))
            self.database = self.client['AAC']
            self.collection = self.database['animals']

        except Exception as e:
            print(e)

    # Insert a single or multiple documents
    def create(self, data):
        try:
            result = False

            # Changed from if data not none. Empty strings are not considered none, and this way is more succinct.
            if data:
                # Single document
                if type(data) == dict:
                    result = self.collection.insert_one(data).acknowledged

                # Multiple documents
                elif type(data) == list:
                    result = self.collection.insert_many(data).acknowledged

            else:
                raise Exception(self.empty_exception)

        # Catch multiple error types (list_exception, empty_exception, type exception, etc.)
        # If data is not of dict type either as a single document or any element of a list,
        # MongoDB will raise its own exception which will be printed here also
        except Exception as e:
            print(e)

        return result

    # Find document(s) from database
    def read(self, query):
        result = False

        try:
            result = self.collection.find(query)

            # Convert from bson to json
            result = json.loads(dumps(result))

            # Convert _id type to string
            for i, _ in enumerate(result):
                result[i]['_id'] = str(result[i]['_id'])

        except Exception as e:
            print(e)

        return result

    # Update document(s)
    def update(self, query, data):
        # Keep existing data (that isn't being updated)
        updated_set = {'$set': data}

        try:
            # Using update_many() allows one or more updates. Used here for simplicity.
            result = self.collection.update_many(query, updated_set)
            return result

        except Exception as e:
            print(e)

    # Delete document(s)
    def delete(self, query):
        try:
            # Using update_many() allows one or more updates. Used here for simplicity.
            result = self.collection.delete_many(query)
            return result

        except Exception as e:
            print(e)

