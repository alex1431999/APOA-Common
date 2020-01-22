"""
This module provides the parent class of all crawl results
"""
import json

from datetime import datetime
from bson import ObjectId

from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes

class CrawlResult():
    """
    Parent class which all crawl results inherit from
    """
    def __init__(self, _id, keyword_ref, keyword_string, language, text, timestamp, crawl_type=CrawlTypes.NEUTRAL.value, processor=None):
        """
        Initialise the crawl result object and try to calculate scores in case
        a processor was added as well

        :param str id: The unique identifier of the crawl result
        :param ObjectId keyword_ref: The ID of the keyword the crawl refers to
        :param str keyword_string: The target keyword that was used to generate the crawl result
        :param str language: The language the text is written in
        :param str text: The actual text that is supposed to be evaluated
        :param datetime timestamp: The timestamp of creation
        :param CrawlType crawl_type: The type of crawl
        :param GoogleCloudLanguageProcessor processor: The NLP processor used to evaluate the text
        """
        # Attributes
        self._id = _id
        self.keyword_ref = keyword_ref
        self.keyword_string = keyword_string
        self.language = language
        self.text = text
        self.crawl_type = crawl_type
        self.timestamp = timestamp

        # Processed data
        self.score = None
        self.entities = []
        self.calculate_score(processor)


    def calculate_score(self, processor=None, force=False):
        """
        Calculate the score if a processor was provided to calculate the score

        This function expects that the processor has a function called "process"
        with the parameters "text: string, keyword_string: string" to be able
        to proecess the data

        :param obj processor: The processor used to calculate the score
        :param boolean force: Force the recalculation of a score
        """
        if processor:
            if (force or self.score is None):
                score, entities, categories = processor.process(self.text, self.keyword_string)
                self.score = score
                self.entities = entities
                self.categories = categories
        else:
            self.score = None
            self.entities = []
            self.categories = []

    def get_score(self):
        """
        Get the score, can be overriden by child classes
        Default behavior just returns the current score
        """
        return self.score

    @staticmethod
    def from_dict(dict_input):
        """
        Cast dict to Crawl Result object
        
        :param dict dict_input: The to be casted dict
        """
        if not dict_input:
            return None
        
        return CrawlResult(
            dict_input['_id'] if type(dict_input['_id']) is ObjectId else ObjectId(dict_input['_id']),
            dict_input['keyword_ref'] if type(dict_input['keyword_ref']) is ObjectId else ObjectId(dict_input['keyword_ref']),
            dict_input['keyword_string'],
            dict_input['language'],
            dict_input['text'],
            dict_input['timestamp']
        )

    def to_json(self):
        """
        Cast the object to JSON

        The plain __dict__ function will not cast the _id to string which can
        be an issue if you are trying to send the object to an API.
        Furthermore the __dict__ function doesn't actually produce a copy
        of the object which means that if you edit the dict it will also
        affect the initial object.
        """
        self._id = str(self._id) if type(self._id) is ObjectId else self._id
        self.keyword_ref = str(self.keyword_ref) if type(self.keyword_ref) is ObjectId else self.keyword_ref
        self.timestamp = self.timestamp.isoformat() if type(self.timestamp) is datetime else self.timestamp
        result =  json.loads(json.dumps(self.__dict__))
        self._id = ObjectId(self._id)
        self.keyword_ref = ObjectId(self.keyword_ref)
        return result
        

    def __str__(self):
        return '<{}> {} --> Type: {}, Score: {}'.format(self._id, self.keyword_string, self.crawl_type, self.score)
