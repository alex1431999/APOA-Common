"""
Module to implement the database interaction functionality
"""

from pymongo import MongoClient

class DBMongoController():
    """
    Class to handle the database interactions

    :param str connection_string: The address of the database
    :param str db_name: The name of the databse
    """
    def __init__(self, connection_string='mongodb://localhost:27017', db_name='default_db'):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

        # By default use the default collection names
        self.set_collections()

    def set_db(self, db_name):
        """
        Set the current database

        :param str db_name: The name of the new databse
        """
        self.db = self.client[db_name]

    def set_collections(self, keyword_collection_name='keyword', crawl_collection_name='crawl'):
        """
        Set custom collection names
        """
        self.keyword_collection = self.db[keyword_collection_name]
        self.crawl_collection = self.db[crawl_collection_name]

    def add_keyword(self, keyword_string, language):
        """
        Add a new keyword document to the database
        """
        document = { 'keyword': keyword_string, 'language': language }
        return self.keyword_collection.insert_one(document)

    def get_keyword(self, keyword_string, language):
        """
        Get a keyword object from the database
        """
        query = { 'keyword': keyword_string, 'language': language }
        return self.keyword_collection.find_one(query)

    def __str__(self):
        return 'Currently connected to "{}" using database "{}"'.format(self.client.HOST, self.db.name)


if __name__ == '__main__':
    db_mongo_controller = DBMongoController()
    print(db_mongo_controller.get_keyword('test', 'EN'))
