"""
This module provides the parent class of all crawl results
"""

class CrawlResult():
    """
    Parent class which all crawl results inherit from
    """
    def __init__(self, _id, keyword_string, language, text, crawl_type, timestamp, processor=None):
        """
        Initialise the crawl result object and try to calculate scores in case
        a processor was added as well

        :param str id: The unique identifier of the crawl result
        :param str keyword_string: The target keyword that was used to generate the crawl result
        :param str language: The language the text is written in
        :param str text: The actual text that is supposed to be evaluated
        :param CrawlType crawl_type: The type of crawl
        :param datetime timestamp: The timestamp of creation
        :param GoogleCloudLanguageProcessor processor: The NLP processor used to evaluate the text
        """
        # Attributes
        self._id = _id
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

        :param obj processor: The processor used to calculate the score
        :param bool force: Force the recalculation of a score
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

    def __str__(self):
        return '<{}> {} --> Type: {}, Score: {}'.format(self._id, self.keyword_string, self.crawl_type, self.score)