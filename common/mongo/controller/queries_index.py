"""
Indexes are accumulations of keywords, they are designed after stock market indexes
"""
from common.mongo.data_types.index import Index
from bson import ObjectId

from common.mongo.decorators.validation import validate_id
from common.mongo.data_types.index import Index


@validate_id("_id")
def get_index_by_id(self, _id: ObjectId, cast=False):
    query = {"_id": str(_id)}

    index = self.indexes_collection.find_one(query)

    if cast:
        return Index.from_dict(index)
    return index


def get_index(self, name: str, cast=False):
    query = {"name": name}

    index = self.indexes_collection.find_one(query)

    if cast:
        return Index.from_dict(index)
    return index


def add_index(self, name: str, user_name: str, return_object=False, cast=False):
    index_exists = self.get_index(name)

    if index_exists:
        query = {"_id": index_exists["_id"]}
        update = {"$addToSet": {"users": user_name}, "$set": {"deleted": False}}

        self.indexes_collection.update_one(query, update)
    else:
        index = {
            "name": name,
            "users": [user_name],
            "deleted": False,
        }

        self.indexes_collection.insert_one(index)

    if return_object:
        index = self.get_index(name)
        return Index.from_dict(index) if cast else index
