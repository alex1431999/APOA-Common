"""
This module deals with queries related to all the meta collections

Meta data is any data that is set by an admin to store data in the database that should only
be changed by admins

There is only ONE object in this collection
"""


def set_meta_keywords_public_ids(
    self, keywords_public_ids: list, return_object=False
) -> dict:
    query = {}
    update = {"$set": {"keywords_public_ids": keywords_public_ids}}

    update_result = self.meta_collection.update_one(query, update, upsert=True)

    if return_object:
        return self.get_meta_keywords_public_ids()
    return update_result


def get_meta_keywords_public_ids(self) -> dict:
    query = {}
    projection = {"keywords_public_ids": 1}

    meta = self.meta_collection.find_one(query, projection)

    return meta["keywords_public_ids"]


def is_meta_initialised(self) -> bool:
    query = {}

    exists = self.meta_collection.find_one(query)

    return True if exists else False
