"""
This module provides the parent class of all crawl results
"""
import json

from datetime import datetime
from bson import ObjectId
from typing import Union

from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes


class CrawlResult:
    """
    Parent class which all crawl results inherit from
    """

    def __init__(
        self,
        _id: Union[str, ObjectId],
        keyword_ref: ObjectId,
        keyword_string: str,
        language: str,
        text: str,
        timestamp: datetime,
        crawl_type=CrawlTypes.NEUTRAL.value,
        score=None,
        entities=None,
        categories=None,
    ):
        """
        Initialise the crawl result object and try to calculate scores in case
        a processor was added as well
        """
        # Attributes
        if categories is None:
            categories = []
        if entities is None:
            entities = []

        self._id = _id
        self.keyword_ref = keyword_ref
        self.keyword_string = keyword_string
        self.language = language
        self.text = text
        self.crawl_type = crawl_type
        self.timestamp = timestamp
        self.score = score
        self.entities = entities
        self.categories = categories

    @staticmethod
    def from_dict(dict_input: dict):
        """
        Cast dict to Crawl Result object
        """
        if not dict_input:
            return None

        return CrawlResult(
            dict_input["_id"]
            if type(dict_input["_id"]) is ObjectId
            else ObjectId(dict_input["_id"]),
            dict_input["keyword_ref"]
            if type(dict_input["keyword_ref"]) is ObjectId
            else ObjectId(dict_input["keyword_ref"]),
            dict_input["keyword_string"],
            dict_input["language"],
            dict_input["text"],
            dict_input["timestamp"],
            entities=dict_input["entities"],
            categories=dict_input["categories"],
        )

    def to_json(self) -> dict:
        """
        Cast the object to JSON

        The plain __dict__ function will not cast the _id to string which can
        be an issue if you are trying to send the object to an API.
        Furthermore the __dict__ function doesn't actually produce a copy
        of the object which means that if you edit the dict it will also
        affect the initial object.
        """
        self._id = str(self._id) if type(self._id) is ObjectId else self._id
        self.keyword_ref = (
            str(self.keyword_ref)
            if type(self.keyword_ref) is ObjectId
            else self.keyword_ref
        )
        self.timestamp = (
            self.timestamp.isoformat()
            if type(self.timestamp) is datetime
            else self.timestamp
        )
        result = json.loads(json.dumps(self.__dict__))
        self._id = ObjectId(self._id)
        self.keyword_ref = ObjectId(self.keyword_ref)
        return result

    def __str__(self) -> str:
        return "<{}> {} --> Type: {}, Score: {}".format(
            self._id, self.keyword_string, self.crawl_type, self.score
        )
