"""
MongoDb data type
"""

class Keyword():
    """
    This class carries a keyword result from the mongodb database
    """
    def __init__(self, _id, keyword_string, language):
        """
        Initialise the object

        :param ObjectId _id: The Id of the document in the database
        :param str keyword_string: The target keyword
        :param str language: The target language
        """
        # Initial Data
        self._id = _id
        self.keyword_string = keyword_string
        self.language = language

    @staticmethod
    def mongo_result_to_keyword(mongo_result):
        """
        Conver a mongo dict to a Keyword object

        :param dict mongo_result: The dict returned by a mongo query
        """
        return Keyword(
            mongo_result['_id'],
            mongo_result['keyword_string'],
            mongo_result['language']
        )

    def __str__(self):
        return "{} ({})".format(self.keyword_string, self.language)
