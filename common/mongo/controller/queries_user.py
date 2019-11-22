"""
This module handles all user database interactions
"""

from passlib.hash import pbkdf2_sha512
from datetime import datetime

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
    
