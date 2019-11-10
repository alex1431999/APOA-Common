"""
All database schemas are defined here.
The schemas are picked up by the controller and applied to the database
if you call the configuration function of the controller.
This way the database iteself will have to deal with validation.
"""

# Use to order the query dict
from collections import OrderedDict

def schema_keyword(collection_name):
    """
    Schema and restrictions of the keywords collection

    :param str collection_name: The collection name of the keywords collection
    """
    vexpr = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['keyword', 'language'],
            'properties': {
                'keyword': {
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
                    'bsonType': 'int',
                    'description': 'must be a int and is required'
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
