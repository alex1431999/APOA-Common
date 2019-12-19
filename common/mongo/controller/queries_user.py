"""
This module handles all user database interactions
"""

from passlib.hash import pbkdf2_sha512
from datetime import datetime

from common.mongo.data_types.user import User

def add_user(self, username, password, is_hashed=False):
    """
    Hashes input password and adds new user to the database

    :param str username: The username of the new user
    :param str password: The password of the new user
    :param boolean is_hashed: Is the password hashed yet?
    """
    if not is_hashed:
        password = pbkdf2_sha512.encrypt(password)

    today = datetime.now() # Time of creation

    document = {
        'username': username,
        'password': password,
        'created_at': today
    }
    
    return self.users_collection.insert_one(document)

def get_user(self, username):
    """
    Get a user from the database

    :param str username: The username of the user
    """
    query = { 'username': username }

    user_dict = self.users_collection.find_one(query)

    if user_dict:
        return User.from_dict(user_dict)
    else:
        return None
    
