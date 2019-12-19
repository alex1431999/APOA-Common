"""
MongoDb data type
"""

class Keyword():
    """
    This class carries a keyword result from the mongodb database
    """
    def __init__(self, _id, keyword_string, language, users=[]):
        """
        Initialise the object

        :param ObjectId _id: The Id of the document in the database
        :param str keyword_string: The target keyword
        :param str language: The target language
        :param list<str> users: All users associated to the keyword 
        """
        # Initial Data
        self._id = _id
        self.keyword_string = keyword_string
        self.language = language
        self.users = users

    @staticmethod
    def mongo_result_to_keyword(mongo_result):
        """
        Convert a mongo dict to a Keyword object

        :param dict mongo_result: The dict returned by a mongo query
        """
        if not mongo_result:
            return None

        return Keyword(
            mongo_result['_id'],
            mongo_result['keyword_string'],
            mongo_result['language'],
            mongo_result['users'],
        )

    @property
    def deleted(self):
        return len(self.users) == 0

    def to_json(self):
        """
        Return a json representation of yourself
        """
        return {
            '_id': self._id,
            'keyword_string': self.keyword_string,
            'language': self.language,
            'users': self.users,
        }

    def __str__(self):
        return "{} ({})".format(self.keyword_string, self.language)
