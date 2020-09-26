"""
All keyword database functionality is defined in this module

TODO:
    - Add function to add index to a keyword
    - Add function to remove index from keyword
    - Add function to get all keywords of an index type
    - Think about removing any access logic from this layer and only check permission on an api level
        - This could allow you to permission a user if he is either directly or indirectly linked to the keyword
"""
from bson import ObjectId
from pymongo.results import UpdateResult

from common import config
from common.exceptions.parameters import UnsupportedLanguageError
from common.mongo.data_types.keyword import Keyword
from common.mongo.decorators.validation import validate_id


@validate_id("_id")
def _set_deleted_flag(self, _id: ObjectId):
    """
    Set the deleted flag of a keyword.
    This will usually be called after a keyword was altered
    """

    keyword = self.get_keyword_by_id(_id, cast=True)

    query = {"_id": _id}
    update = {"$set": {"deleted": keyword.deleted}}

    self.keywords_collection.update_one(query, update)


def add_keyword(
    self,
    keyword_string: str,
    language: str,
    username: str,
    return_object=False,
    cast=False,
):
    """
    Add a new keyword document to the database
    """
    if language not in config.SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageError(language)

    # Try to find the keyword
    query = {"keyword_string": keyword_string, "language": language}
    keyword_dict = self.keywords_collection.find_one(query)

    if keyword_dict:  # Add username to users of keyword
        query = {"_id": keyword_dict["_id"]}
        update = {"$addToSet": {"users": username}}

        update_result = self.keywords_collection.update_one(query, update)

        self._set_deleted_flag(keyword_dict["_id"])

        result = update_result
    else:  # Create a new keyword
        document = {
            "keyword_string": keyword_string,
            "language": language,
            "users": [username],
            "indexes": [],
            "deleted": False,
        }

        result = self.keywords_collection.insert_one(document)

    if return_object:
        result = self.get_keyword(keyword_string, language, username, cast=cast)

    return result


def get_keyword(self, keyword_string: str, language: str, username=None, cast=False):
    """
    Get a keyword object from the database
    """
    query = {"keyword_string": keyword_string, "language": language}

    if username:  # If a username was passded
        query["users"] = username  # Make sure the username is associated to the keyword

    keyword = self.keywords_collection.find_one(query)

    if keyword and cast:
        keyword = Keyword.from_dict(keyword)

    return keyword


def get_keywords_user(self, username: str, cast=False):
    """
    Get the keywords of a particular username
    """
    query = {"users": username}

    keywords = list(self.keywords_collection.find(query))

    if cast:  # You might want have all of the keywords casted
        keywords = [Keyword.from_dict(mongo_result) for mongo_result in keywords]

    return keywords


def get_keyword_by_id(self, _id: ObjectId, username=None, cast=False):
    """
    Get a keyword via its ID
    """
    query = {"_id": _id}

    if username:
        query["users"] = username

    keyword = self.keywords_collection.find_one(query)

    if cast:
        keyword = Keyword.from_dict(keyword)

    return keyword


@validate_id("_id")
def delete_keyword(self, _id: ObjectId, username: str) -> UpdateResult:
    """
    Delete a user from a keyword given the ID
    """
    query = {"_id": _id}
    update = {"$pull": {"users": username}}

    deletion = self.keywords_collection.update_one(query, update)

    self._set_deleted_flag(_id)

    return deletion


def get_keyword_batch_cursor(self):
    """
    Get all outdated keywords which are in need of new twitter results

    :return: A cursor with batches of size 100
    :rtype: RawBatchCurosor
    """
    cursor = self.keywords_collection.find_raw_batches(no_cursor_timeout=True)
    return cursor


def get_keywords_public(self, cast=False) -> list:
    keywords_public_ids = self.get_meta_keywords_public_ids()

    # Only add keywords which are not None
    keywords = []
    for _id in keywords_public_ids:
        keyword = self.get_keyword_by_id(_id, cast=cast)
        if keyword:
            keywords.append(keyword)

    return keywords


@validate_id(["keyword_id", "index_id"])
def add_index_to_keyword(self, keyword_id: ObjectId, index_id: ObjectId, return_object=False, cast=False):
    query = {"_id": keyword_id}
    update = {"$addToSet": {"indexes": index_id}}

    self.keywords_collection.update_one(query, update)

    if return_object:
        return self.get_keyword_by_id(keyword_id, cast=cast)