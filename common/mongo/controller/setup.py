"""
All general mongo controller methods are defined in here
"""

from pymongo import ASCENDING

from common.mongo import schemas

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
    self.db.command(schemas.schema_keywords(self.keywords_collection.name))
    self.db.command(schemas.schema_crawls_twitter(self.crawls_twitter_collection.name))
    self.db.command(schemas.schema_users(self.users_collection.name))

    # Apply indexes
    # Keywords collection
    self.keywords_collection.create_index([('keyword_string', ASCENDING), ('language', ASCENDING)], unique=True)

    # Crawls Twitter collection
    self.crawls_twitter_collection.create_index([('tweet_id', ASCENDING)], unique=True)

    # Users collection
    self.users_collection.create_index([('username', ASCENDING)], unique=True)

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

def set_collections(
        self, 
        keywords_collection_name='keywords', 
        crawls_twitter_collection_name='crawls_twitter',
        users_collection_name='users' 
    ):
    """
    Set custom collection names

    :param str keywords_collection_name: The name of the keyword collection
    :param str crawls_twitter_collection_name: The name of the twitter crawl collection
    :param str users_collection_name: The name of the users collection
    """
    self.keywords_collection = self.create_collection_if_not_exists(keywords_collection_name)
    self.crawls_twitter_collection = self.create_collection_if_not_exists(crawls_twitter_collection_name)
    self.users_collection = self.create_collection_if_not_exists(users_collection_name)

@property
def crawls_collections(self):
    """
    Gather all the crawl collections in one array.
    All of them have similar properties and therefore it's useful to group
    them together for the processor. 

    If a new crawl collection is added to the system, make sure to add that 
    collection to this list such that the processor will also process that collection.

    :return: All crawl collections
    :rtype: List <Collection>
    """
    return [
        self.crawls_twitter_collection,
    ]
