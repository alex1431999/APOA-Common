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
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["keyword_string", "language", "users", "deleted"],
            "properties": {
                "keyword_string": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                },
                "language": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                },
                "users": {
                    "bsonType": "array",
                    "description": "must be an array of strings and is required",
                },
                "deleted": {
                    "bsonType": "bool",
                    "description": "must be a boolean and defaults to false",
                },
            },
        }
    }
    query = [
        ("collMod", collection_name),
        ("validator", vexpr),
        ("validationLevel", "moderate"),
    ]
    query = OrderedDict(query)
    return query


def schema_crawls(collection_name):
    """
    Schema and restrictions of the crawls collection

    :param str collection_name: The name of the crawls collection
    :return: The query to be inserted into pymongo to enable the schema
    :rtype: OrderedDict
    """
    vexpr = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "keyword_ref",
                "text",
                "timestamp",
                "crawl_type",
                "entities",
                "categories",
            ],
            "properties": {
                "keyword_ref": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required",
                },
                "text": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                },
                "timestmap": {
                    "bsonType": "date",
                    "description": "must be a date and is required",
                },
                "crawl_type": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                },
                "entities": {
                    "bsonType": "array",
                    "description": "must be an array and is required",
                },
                "categories": {
                    "bsonType": "array",
                    "description": "must be an array and is required",
                },
            },
        }
    }
    query = [
        ("collMod", collection_name),
        ("validator", vexpr),
        ("validationLevel", "moderate"),
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
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "password", "created_at"],
            "properties": {
                "username": {
                    "bsonType": "string",
                    "description": "must be string and is required",
                },
                "password": {
                    "bsonType": "string",
                    "description": "must be string and is required",
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "must be date and is required",
                },
            },
        }
    }
    query = [
        ("collMod", collection_name),
        ("validator", vexpr),
        ("validationLevel", "moderate"),
    ]
    query = OrderedDict(query)
    return query
