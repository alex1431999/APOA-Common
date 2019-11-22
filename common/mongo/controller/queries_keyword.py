"""
All keyword database functionality is defined in this module
"""

from common.mongo.data_types.keyword import Keyword
from common import config

def add_keyword(self, keyword_string, language):
    """
    Add a new keyword document to the database

    :param str keyword_string: The target keyword
    :param str language: The language the keyword is written in
    :return: The inserted document result
    :rtype: InsertOneResult
    """
    if (language not in config.SUPPORTED_LANGUAGES):
        raise Exception('Unsupported language "{}"'.format(language))

    document = { 'keyword_string': keyword_string, 'language': language }
    return self.keywords_collection.insert_one(document)

def get_keyword(self, keyword_string, language):
    """
    Get a keyword object from the database

    :param str keyword_string: The target keyword
    :param str language: The language the keyword is written in
    :return: The found keyword
    :rtype: Keyword or None
    """
    query = { 'keyword_string': keyword_string, 'language': language }
    keyword_dict = self.keywords_collection.find_one(query)
    if (keyword_dict):
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
