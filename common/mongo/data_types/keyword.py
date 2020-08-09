"""
MongoDb data type
"""

from bson import ObjectId


class Keyword:
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
    def from_dict(dict_input):
        """
        Convert a mongo dict to a Keyword object

        :param dict dict_input: The to be casted dict
        """
        if not dict_input:
            return None

        return Keyword(
            dict_input["_id"]
            if type(dict_input["_id"]) is ObjectId
            else ObjectId(dict_input["_id"]),
            dict_input["keyword_string"],
            dict_input["language"],
            dict_input["users"],
        )

    @property
    def deleted(self):
        return len(self.users) == 0

    def to_json(self):
        """
        Return a json representation of yourself
        """
        return {
            "_id": self._id if type(self._id) is not ObjectId else str(self._id),
            "keyword_string": self.keyword_string,
            "language": self.language,
            "users": self.users,
        }

    def __str__(self):
        return "{} ({})".format(self.keyword_string, self.language)
