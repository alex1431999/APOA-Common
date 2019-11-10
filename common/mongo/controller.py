"""
Module to implement the database interaction functionality
"""

from pymongo import MongoClient, ASCENDING

from common.mongo.data_types.keyword import Keyword
from common.mongo import schemas
from common import config

class MongoController():
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

    def configure_database(self):
        """
        Add basic configurations to the database
        This only needs to be called once when the database
        is freshly created
        """
        # Apply schemas
        self.db.command(schemas.schema_keyword(self.keywords_collection.name))
        self.db.command(schemas.schema_crawls_twitter(self.crawls_twitter_collection.name))

        # Apply indexes
        # Keywords collection
        self.keywords_collection.create_index([('keyword_string', ASCENDING), ('language', ASCENDING)], unique=True)

        # Crawls Twitter collection
        self.crawls_twitter_collection.create_index([('tweet_id', ASCENDING)], unique=True)

    def create_collection_if_not_exists(self, collection_name):
        """
        Check if a collection exists, if not, add the collection

        :param str collection_name: The name of the new collection
        :return: The created / existing collection
        :rtype: Collection
        """
        if collection_name not in self.db.list_collection_names():
            return self.db.create_collection(collection_name)
        else:
            return self.db[collection_name]

    def set_collections(self, keywords_collection_name='keywords', crawls_twitter_collection_name='crawls_twitter'):
        """
        Set custom collection names

        :param str keywords_collection_name: The name of the keyword collection
        :param str crawls_twitter_collection_name: The name of the twitter crawl collection
        """
        self.keywords_collection = self.create_collection_if_not_exists(keywords_collection_name)
        self.crawls_twitter_collection = self.create_collection_if_not_exists(crawls_twitter_collection_name)

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
            return Keyword(keyword_dict)
        return None

    def get_keyword_batch_cursor(self):
        """
        Get all outdated keywords which are in need of new twitter results

        :return: A cursor with batches of size 100
        :rtype: RawBatchCurosor
        """
        cursor = self.keywords_collection.find_raw_batches(no_cursor_timeout=True)
        return cursor

    def add_crawl_twitter(self, keyword_id, tweet_id, text, likes, retweets, timestamp):
        """
        Add a new twitter crawl to the crawl twitter collection
        If the tweet already exists, update the document

        :param ObjectId keyword_id: The id of the target keyword used
        :param long tweet_id: The id of the tweet provided by twitter
        :param str text: The tweet text
        :param int likes: The amount of likes the tweet has received
        :param int retweets: The amount of retweets the tweet has received
        :param date timestamp: The time the tweet was created
        :return: The update result
        :rtype: UpdateResult
        """
        document = {
            'keyword_ref': keyword_id,
            'tweet_id': tweet_id,
            'text': text,
            'likes': likes,
            'retweets': retweets,
            'timestamp': timestamp,
        }

        query = { 'tweet_id': tweet_id }

        return self.crawls_twitter_collection.replace_one(query, document, upsert=True)

    def __str__(self):
        return 'Currently connected to "{}" using database "{}"'.format(self.client.HOST, self.db.name)
