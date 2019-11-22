"""
All keyword database functionality is defined in this module
"""

from common.mongo.data_types.keyword import Keyword
from common import config

def add_keyword(self, keyword_string, language, user):
    """
    Add a new keyword document to the database

    :param str keyword_string: The target keyword
    :param str language: The language the keyword is written in
    :return: The inserted document result
    :rtype: InsertOneResult / UpdateOneResult
    """
    if (language not in config.SUPPORTED_LANGUAGES):
        raise Exception('Unsupported language "{}"'.format(language))
    
    # Try to find the keyword
    query = { 'keyword_string': keyword_string, 'language': language }
    keyword_dict = self.keywords_collection.find_one(query)

    if keyword_dict: # Add user to users of keyword
        query = { '_id': keyword_dict['_id'] }
        update = { '$addToSet': {'users': user } }
        return self.keywords_collection.update_one(query, update)
    else: # Create a new keyword
        document = { 'keyword_string': keyword_string, 'language': language, 'users': [user] }
        return self.keywords_collection.insert_one(document)

def get_keyword(self, keyword_string, language, user=None):
    """
    Get a keyword object from the database

    :param str keyword_string: The target keyword
    :param str language: The language the keyword is written in
    :param str user: There might be a user that requested this keyword
    :return: The found keyword
    :rtype: Keyword or None
    """
    query = { 'keyword_string': keyword_string, 'language': language }

    if user: # If a user was passded
        query['users'] = user # Make sure the user is associated to the keyword

    keyword_dict = self.keywords_collection.find_one(query)
    if keyword_dict:
        return Keyword.mongo_result_to_keyword(keyword_dict)
    return None

def get_keyword_batch_cursor(self):
    """
    Get all outdated keywords which are in need of new twitter results

    :return: A cursor with batches of size 100
    :rtype: RawBatchCurosor
    """
    cursor = self.keywords_collection.find_raw_batches(no_cursor_timeout=True)
    return cursor
