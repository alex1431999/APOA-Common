"""
MongoDb data type
"""

from bson import ObjectId


class Keyword:
    """
    This class carries a keyword result from the mongodb database
    """

    def __init__(
        self,
        _id: ObjectId,
        keyword_string: str,
        language: str,
        users=None,
        indexes=None,
    ):
        """
        Initialise the object
        """
        # Initial Data
        if indexes is None:
            indexes = []
        if users is None:
            users = []

        self._id = _id
        self.keyword_string = keyword_string
        self.language = language
        self.users = users
        self.indexes = indexes

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
            dict_input["indexes"],
        )

    @property
    def deleted(self):
        return len(self.users) == 0 and len(self.indexes) == 0

    def to_json(self):
        """
        Return a json representation of yourself
        """
        return {
            "_id": self._id if type(self._id) is not ObjectId else str(self._id),
            "keyword_string": self.keyword_string,
            "language": self.language,
            "users": self.users,
            "indexes": self.indexes,
        }

    def __str__(self):
        return "{} ({})".format(self.keyword_string, self.language)
