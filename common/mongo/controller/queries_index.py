"""
Indexes are accumulations of keywords, they are designed after stock market indexes
"""
from bson import ObjectId

from common.exceptions.parameters import UnsupportedIndexTypeError
from common.mongo.decorators.validation import validate_id
from common.mongo.data_types.index import Index, IndexTypes


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


def add_index(
    self,
    name: str,
    index_type: IndexTypes,
    username: str,
    return_object=False,
    cast=False,
):
    index_exists = self.get_index(name)

    if index_exists:
        query = {"_id": index_exists["_id"]}
        update = {"$addToSet": {"users": username}, "$set": {"deleted": False}}

        self.indexes_collection.update_one(query, update)
    else:
        index = {
            "name": name,
            "users": [username],
            "index_type": index_type,
            "deleted": False,
        }

        self.indexes_collection.insert_one(index)

    if return_object:
        index = self.get_index(name)
        return Index.from_dict(index) if cast else index


def get_indexes_by_type(self, index_type: IndexTypes, username: str, cast=False):
    if index_type not in [index_type.value for index_type in IndexTypes]:
        raise UnsupportedIndexTypeError(index_type)

    query = {"index_type": index_type, "users": username}

    indexes = list(self.indexes_collection.find(query))

    if cast:
        indexes = [Index.from_dict(mongo_result) for mongo_result in indexes]

    return indexes
