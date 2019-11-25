"""
All keyword database functionality is defined in this module
"""
from bson import ObjectId

from common.mongo.data_types.keyword import Keyword
from common import config

def _set_deleted_flag(self, _id):
    """
    Set the deleted flag of a keyword.
    This will usually be called after a keyword was altered

    :param ObjectId _id: The ID of the target keyword
    :return: If the deleted flag was set
    :rtype: boolean
    """
    if _id is not ObjectId:
        _id = ObjectId(_id)

    keyword = self.get_keyword_by_id(_id, cast=True)
    
    if len(keyword.users) == 0:
        query = { '_id': _id }
        update = { '$set': { 'deleted': True } }
        
        self.keywords_collection.update_one(query, update)
        return True

    return False


def add_keyword(self, keyword_string, language, username):
    """
    Add a new keyword document to the database

    :param str keyword_string: The target keyword
    :param str language: The language the keyword is written in
    :param str username: The name of the user that is added to the keyword
    :return: The inserted document result
    :rtype: InsertOneResult / UpdateOneResult
    """
    if (language not in config.SUPPORTED_LANGUAGES):
        raise Exception('Unsupported language "{}"'.format(language))
    
    # Try to find the keyword
    query = { 'keyword_string': keyword_string, 'language': language }
    keyword_dict = self.keywords_collection.find_one(query)

    if keyword_dict: # Add username to users of keyword
        query = { '_id': keyword_dict['_id'] }
        update = { '$addToSet': {'users': username } }
        return self.keywords_collection.update_one(query, update)
    else: # Create a new keyword
        document = { 
            'keyword_string': keyword_string, 
            'language': language, 
            'users': [username], 
            'deleted': False,
        }
        return self.keywords_collection.insert_one(document)

def get_keyword(self, keyword_string, language, username=None):
    """
    Get a keyword object from the database

    :param str keyword_string: The target keyword
    :param str language: The language the keyword is written in
    :param str username: There might be a username that requested this keyword
    :return: The found keyword
    :rtype: Keyword or None
    """
    query = { 'keyword_string': keyword_string, 'language': language }

    if username: # If a username was passded
        query['users'] = username # Make sure the username is associated to the keyword

    keyword_dict = self.keywords_collection.find_one(query)
    if keyword_dict:
        return Keyword.mongo_result_to_keyword(keyword_dict)
    return None

def get_keywords_user(self, username, cast=False):
    """
    Get the keywords of a particular username

    :param str username: The username of the username
    :param boolean cast: If True, cast all results to be of type Keyword
    :return: All keywords that belong to a username
    :rtype: List<Keyword> / List<dict>
    """
    query = { 'users': username }
    projection = { '_id': 1, 'keyword_string': 1, 'language': 1 }

    keywords = list(self.keywords_collection.find(query, projection))
    
    if cast: # You might want have all of the keywords casted
        keywords = [Keyword.mongo_result_to_keyword(mongo_result) for mongo_result in keywords]
    
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

    query = { '_id': _id }

    if username:
        query['users'] = username
    
    keyword = self.keywords_collection.find_one(query)

    if cast:
        keyword = Keyword.mongo_result_to_keyword(keyword)
    
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

    query = { '_id': _id }
    update = { '$pull': { 'users': username } }

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
