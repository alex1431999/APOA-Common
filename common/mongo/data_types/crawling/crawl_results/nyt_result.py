"""
This module provides the implementation of the News Crawl result class
"""

from bson import ObjectId

from common.mongo.data_types.crawling.crawl_result import CrawlResult
from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes


class NytResult(CrawlResult):
    """
    This class serves the purpose of holding New York Times crawl result data

    TODO:
        - Still missing timestamp identifier
    """

    def __init__(
        self,
        _id,
        article_id,
        keyword_ref,
        keyword_string,
        language,
        text,
        timestamp,
        score=None,
        entities=None,
        categories=None,
    ):
        """
        Set up all attributes

        :param str _id: The ID of the tweet given by MongoDB
        :param str article_id: The ID provided by NYT
        :param ObjectId keyword_ref: The ID of the keyword which was used to generate the article
        :param str keyword_string: The target keyword that was used to generate the crawl result
        :param str language: The language the text is written in
        :param str text: A snippet of the Article
        :param str timestamp: The date on which the article was published
        """
        super().__init__(
            _id,
            keyword_ref,
            keyword_string,
            language,
            text,
            timestamp,
            CrawlTypes.NYT.value,
            score,
            entities,
            categories,
        )
        if categories is None:
            categories = []
        if entities is None:
            entities = []

        self.article_id = article_id

    @staticmethod
    def from_dict(dict_input):
        """
        Convert a mongo result into a NYT Result Object

        :param dict dict_input: The to be casted dict
        """
        if not dict_input:
            return None

        score = None
        if "score" in dict_input:
            score = dict_input["score"]

        return NytResult(
            dict_input["_id"]
            if type(dict_input["_id"]) is ObjectId
            else ObjectId(dict_input["_id"]),
            dict_input["article_id"],
            dict_input["keyword_ref"]
            if type(dict_input["keyword_ref"]) is ObjectId
            else ObjectId(dict_input["keyword_ref"]),
            dict_input["keyword_string"],
            dict_input["language"],
            dict_input["text"],
            dict_input["timestamp"],
            score=score,
            entities=dict_input["entities"],
            categories=dict_input["categories"],
        )
