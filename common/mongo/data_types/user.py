"""
MongoDb data type
"""

from passlib.hash import pbkdf2_sha512

class User():
    """
    This class carries a user result from the mongodb database
    """
    def __init__(self, _id, username, password, created_at):
        """
        Set attributes

        :param ObjectId _id: The id of the database object
        :param str username: The username of the user
        :param str password: The hashed password of the user
        :param datetime created_at: The time of creation
        """
        self._id = _id
        self.username = username
        self.password = password
        self.created_at = created_at

    @staticmethod
    def mongo_result_to_user(mongo_result):
        """
        Convert a mongo dict to a Keyword object

        :param dict mongo_result: The dict returned by a mongo query
        """
        if not mongo_result:
            return None

        return User(
            mongo_result['_id'],
            mongo_result['username'],
            mongo_result['password'],
            mongo_result['created_at'],
        )

    def verifiy(self, password_candidate):
        """
        Verify if a password candidate is the correct password

        :param str password_candidate: The clear text password that shall be verified
        """
        return pbkdf2_sha512.verify(password_candidate, self.password)

    def __str__(self):
        return "{} ({})".format(self.username, self.created_at)
