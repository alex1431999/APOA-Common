"""
All keyword database functionality is defined in this module
"""
from bson import ObjectId

from common import config
from common.exceptions.parameters import UnsupportedLanguageError
from common.mongo.data_types.keyword import Keyword


def _set_deleted_flag(self, _id):
    """
    Set the deleted flag of a keyword.
    This will usually be called after a keyword was altered

    :param ObjectId _id: The ID of the target keyword
    """
    if _id is not ObjectId:
        _id = ObjectId(_id)

    keyword = self.get_keyword_by_id(_id, cast=True)

    query = {"_id": _id}
    update = {"$set": {"deleted": keyword.deleted}}

    self.keywords_collection.update_one(query, update)


def add_keyword(
    self, keyword_string, language, username, return_object=False, cast=False
):
    """
    Add a new keyword document to the database

    :param str keyword_string: The target keyword
    :param str language: The language the keyword is written in
    :param str username: The name of the user that is added to the keyword
    :param boolean return_object: If true return the updated object
    :param boolean cast: If true cast the returned object to Keyword
    :return: The inserted document result
    :rtype: InsertOneResult / UpdateOneResult
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
            "deleted": False,
        }

        result = self.keywords_collection.insert_one(document)

    if return_object:
        result = self.get_keyword(keyword_string, language, username, cast=cast)

    return result


def get_keyword(self, keyword_string, language, username=None, cast=False):
    """
    Get a keyword object from the database

    :param str keyword_string: The target keyword
    :param str language: The language the keyword is written in
    :param str username: There might be a username that requested this keyword
    :param boolean cast: If true, cast the keyword dict to Keyword
    :return: The found keyword
    :rtype: Keyword or None
    """
    query = {"keyword_string": keyword_string, "language": language}

    if username:  # If a username was passded
        query["users"] = username  # Make sure the username is associated to the keyword

    keyword = self.keywords_collection.find_one(query)

    if keyword and cast:
        keyword = Keyword.from_dict(keyword)

    return keyword


def get_keywords_user(self, username, cast=False):
    """
    Get the keywords of a particular username

    :param str username: The username of the username
    :param boolean cast: If True, cast all results to be of type Keyword
    :return: All keywords that belong to a username
    :rtype: List<Keyword> / List<dict>
    """
    query = {"users": username}
    projection = {"_id": 1, "keyword_string": 1, "language": 1}

    keywords = list(self.keywords_collection.find(query, projection))

    if cast:  # You might want have all of the keywords casted
        keywords = [Keyword.from_dict(mongo_result) for mongo_result in keywords]

    return keywords


def get_keyword_by_id(self, _id, username=None, cast=False):
    """
    Get a keyword via its ID

    :param ObjectId _id: The ID of the keyword
    :param str username: The user who requests the keyword
    :param boolean cast: If True, cast keyword to Keyword
    :return: The Keyword found
    :rtype: Keyword or Dict
    """
    if _id is not ObjectId:
        _id = ObjectId(_id)

    query = {"_id": _id}

    if username:
        query["users"] = username

    keyword = self.keywords_collection.find_one(query)

    if cast:
        keyword = Keyword.from_dict(keyword)

    return keyword


def delete_keyword(self, _id, username):
    """
    Delete a user from a keyword given the ID

    :param ObjectId _id: The ID of the keyword
    :param str username: The user who made the request
    :return: The deletion
    """
    if _id is not ObjectId:
        _id = ObjectId(_id)

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
