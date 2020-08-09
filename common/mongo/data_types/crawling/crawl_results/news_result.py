"""
This module provides the implementation of the News Crawl result class
"""

from bson import ObjectId

from common.mongo.data_types.crawling.crawl_result import CrawlResult
from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes


class NewsResult(CrawlResult):
    """
    This class serves the purpose of holding News crawl result data
    """

    def __init__(
        self,
        _id,
        keyword_ref,
        keyword_string,
        language,
        title,
        author,
        text,
        timestamp,
        score=None,
        entities=[],
        categories=[],
    ):
        """
        Set up all attributes

        :param str _id: The ID associated to the news article
        :param ObjectId keyword_ref: The ID of the keyword which was used to find the article
        :param str keyword_string: The target keyword that was used to generate the crawl result
        :param str language: The language the text is written in
        :param str title: The title of the article
        :param str author: The author of the article
        :param str text: The actual content of the article
        :param datetime timestamp: The timestamp of creation
        """
        super().__init__(
            _id,
            keyword_ref,
            keyword_string,
            language,
            text,
            timestamp,
            CrawlTypes.NEWS.value,
            score,
            entities,
            categories,
        )
        self.author = author

    @staticmethod
    def from_dict(dict_input):
        """
        Convert a mongo result into a News Result Object

        :param dict dict_input: The to be casted dict
        """
        if not dict_input:
            return None

        score = None
        if "score" in dict_input:
            score = dict_input["score"]

        return NewsResult(
            dict_input["_id"]
            if type(dict_input["_id"]) is ObjectId
            else ObjectId(dict_input["_id"]),
            dict_input["keyword_ref"]
            if type(dict_input["keyword_ref"]) is ObjectId
            else ObjectId(dict_input["keyword_ref"]),
            dict_input["keyword_string"],
            dict_input["language"],
            dict_input["title"],
            dict_input["author"],
            dict_input["text"],
            dict_input["timestamp"],
            score=score,
            entities=dict_input["entities"],
            categories=dict_input["categories"],
        )
