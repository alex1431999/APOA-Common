"""
This module provides the implementation of the Twitter Crawl result class
"""

from bson import ObjectId

from common.mongo.data_types.crawling.crawl_result import CrawlResult
from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes


class TwitterResult(CrawlResult):
    """
    This class serves the purpose of holding Twitter
    crawl result data
    """

    def __init__(
        self,
        _id,
        tweet_id,
        keyword_ref,
        keyword_string,
        language,
        text,
        timestamp,
        likes=0,
        retweets=0,
        score=None,
        entities=None,
        categories=None,
    ):
        """
        Set up all attributes

        :param ObjectId _id: The Object ID given by mongodb
        :param long tweet_id: The ID of the tweet given by Twitter
        :param ObjectId keyword_ref: The ID of the keyword which was used to generate the tweet
        :param str keyword_string: The target keyword that was used to generate the crawl result
        :param str language: The language the text is written in
        :param str text: The tweet text
        :param datetime timestamp: The time at which the tweet was posted
        :param int likes: The amount of likes the tweet has received
        :param int retweets: The amount of retweets the tweet has received
        """
        super().__init__(
            _id,
            keyword_ref,
            keyword_string,
            language,
            text,
            timestamp,
            CrawlTypes.TWITTER.value,
            score,
            entities,
            categories,
        )
        self.tweet_id = tweet_id
        self.likes = likes
        self.retweets = retweets

    @staticmethod
    def from_dict(dict_input):
        """
        Convert a mongo result into a Twitter Result object

        :param dict dict_input: The to be casted dict
        """
        if not dict_input:
            return None

        score = None
        if "score" in dict_input:
            score = dict_input["score"]

        return TwitterResult(
            dict_input["_id"]
            if type(dict_input["_id"]) is ObjectId
            else ObjectId(dict_input["_id"]),
            dict_input["tweet_id"],
            dict_input["keyword_ref"]
            if type(dict_input["keyword_ref"]) is ObjectId
            else ObjectId(dict_input["keyword_ref"]),
            dict_input["keyword_string"],
            dict_input["language"],
            dict_input["text"],
            dict_input["timestamp"],
            dict_input["likes"],
            dict_input["retweets"],
            score=score,
            entities=dict_input["entities"],
            categories=dict_input["categories"],
        )
