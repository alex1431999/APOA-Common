"""
This module provides the implementation of the Twitter Crawl result class
"""

from common.mongo.data_types.crawling.crawl_result import CrawlResult
from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes

class TwitterResult(CrawlResult):
    """
    This class serves the purpose of holding Twitter
    crawl result data
    """
    def __init__(self, _id, tweet_id, keyword_string, language, text, timestamp, likes=0, retweets=0, processor=None):
        """
        Set up all attributes

        :param ObjectId _id: The Object ID given by mongodb
        :param long tweet_id: The ID of the tweet given by Twitter
        :param str keyword_string: The target keyword that was used to generate the crawl result
        :param str language: The language the text is written in
        :param str text: The tweet text
        :param datetime timestamp: The time at which the tweet was posted
        :param int likes: The amount of likes the tweet has received
        :param int retweets: The amount of retweets the tweet has received
        """
        super().__init__(_id, keyword_string, language, text, CrawlTypes.TWITTER.value, timestamp, processor)
        self.tweet_id = tweet_id
        self.likes = likes
        self.retweets = retweets

    @staticmethod
    def mongo_result_to_twitter_result(mongo_result):
        """
        Convert a mongo result into a Twitter Result object

        :param dict mongo_result: The returned dict from a mongo query
        """
        return TwitterResult(
            mongo_result['_id'],
            mongo_result['tweet_id'],
            mongo_result['keyword_string'],
            mongo_result['language'],
            mongo_result['text'],
            mongo_result['timestamp'],
            mongo_result['likes'],
            mongo_result['retweets']
        )

    def get_score(self):
        """
        Overriden function from parent class
        Applying likes and retweets to the score
        """
        return self.score * ((self.likes * 0.25) + (self.retweets * 0.75) + 1)
