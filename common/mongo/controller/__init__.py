"""
Module to implement the database interaction functionality

All the functions are implemented within the package, see the remaining files of the package.
The initial class file just grew way too big.
The idea to structre this class in this way comes from this stack overflow post:
https://stackoverflow.com/questions/9155618/splitting-a-class-that-is-too-large
"""

from pymongo import MongoClient, ASCENDING

from common.utils.environment import check_environment 

class MongoController():
    """
    Class to handle the database interactions

    :param str connection_string: The address of the database
    :param str db_name: The name of the databse
    """
    
    """
    Imports
    """

    # General
    from common.mongo.controller.setup import (
        set_db, 
        configure_database, 
        create_collection_if_not_exists, 
        set_collections,
    )

    # Keywords
    from common.mongo.controller.queries_keyword import (
        _set_deleted_flag,
        add_keyword,
        get_keyword,
        get_keywords_user,
        get_keyword_batch_cursor,
        get_keyword_by_id,
        delete_keyword,
    )

    # Crawls
    from common.mongo.controller.queries_crawls import (
        get_unprocessed_crawls,
        set_score_crawl,
        get_crawl_by_id,
        get_crawls_plotting_data,
        get_crawls_average_score,
    )

    # Twitter
    from common.mongo.controller.queries_crawls_twitter import (
        add_crawl_twitter,
        get_crawl_twitter_by_id,
    )

    # News
    from common.mongo.controller.queries_crawls_news import (
        add_crawl_news,
        get_crawl_news,
    )

    # Users
    from common.mongo.controller.queries_user import (
        add_user,
        get_user,
    )

    def __init__(self, connection_string='mongodb://localhost:27017', db_name='default_db'):
        """
        Setup the controller with a connection to the database and all configurations loaded

        :param str connection_string: The URL used to connect to the database
        :param str db_name: The databse which shall be using during runtime
        """
        connection_string = check_environment('MONGO_URL', connection_string)
        db_name = check_environment('MONGO_DATABASE_NAME', db_name)

        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

        # By default use the default collection names
        self.set_collections()

    def __str__(self):
        return 'Currently connected to "{}" using database "{}"'.format(self.client.HOST, self.db.name)
