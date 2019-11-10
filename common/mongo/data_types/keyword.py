"""
MongoDb data type
"""

class Keyword():
    """
    This class carries a keyword result from the mongodb database
    """
    def __init__(self, keyword_dict):
        """
        Initialise the object

        :param dict keyword_dict: The dict returned by Pymongo
        """
        # Initial Data
        self._id = keyword_dict['_id']
        self.keyword_string = keyword_dict['keyword_string']
        self.language = keyword_dict['language']

    def __str__(self):
        return "{} ({})".format(self.keyword_string, self.language)
