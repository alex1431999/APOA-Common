"""
All database schemas are defined here.
The schemas are picked up by the controller and applied to the database
if you call the configuration function of the controller.
This way the database iteself will have to deal with validation.
"""

# Use to order the query dict
from collections import OrderedDict

def schema_keywords(collection_name):
    """
    Schema and restrictions of the keywords collection

    :param str collection_name: The collection name of the keywords collection
    :return: The query to be inserted into pymongo to enable the schema
    :rtype: OrderedDict
    """
    vexpr = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['keyword_string', 'language'],
            'properties': {
                'keyword_string': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'language': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
            }
        }
    }
    query = [
        ('collMod', collection_name),
        ('validator', vexpr),
        ('validationLevel', 'moderate')
    ]
    query = OrderedDict(query)
    return query

def schema_crawls_twitter(collection_name):
    """
    Schema and restrictions of the crawls twitter collection

    :param str collection_name: The name of the crawls twitter collection
    :return: The query to be inserted into pymongo to enable the schema
    :rtype: OrderedDict
    """
    vexpr = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['keyword_ref', 'tweet_id', 'text', 'likes', 'retweets', 'timestamp'],
            'properties': {
                'keyword_ref': {
                    'bsonType': 'objectId',
                    'description': 'must be an objectId and is required'
                },
                'tweet_id': {
                    'bsonType': 'long',
                    'description': 'must be a long and is required'
                },
                'text': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'likes': {
                    'bsonType': 'int',
                    'description': 'must be an int and is required'
                },
                'retweets': {
                    'bsonType': 'int',
                    'description': 'must be an int and is required'
                },
                'timestmap': {
                    'bsonType': 'date',
                    'description': 'must be a date and is required'
                }
            }
        }
    }
    query = [
        ('collMod', collection_name),
        ('validator', vexpr),
        ('validationLevel', 'moderate')
    ]
    query = OrderedDict(query)
    return query

def schema_users(collection_name):
    """
    Schema and restrictions of the user collection

    :param str collection_name: The name of the crawls twitter collection
    :return: The query to be inserted into pymongo to enable the schema
    :rtype: OrderedDict
    """
    vexpr = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['username', 'password', 'created_at'],
            'properties': {
                'username': {
                    'bsonType': 'string',
                    'description': 'must be string and is required'
                },
                'password': {
                    'bsonType': 'string',
                    'description': 'must be string and is required'
                },
                'created_at': {
                    'bsonType': 'date',
                    'description': 'must be date and is required'
                }
            }
        }
    }
    query = [
        ('collMod', collection_name),
        ('validator', vexpr),
        ('validationLevel', 'moderate')
    ]
    query = OrderedDict(query)
    return query
