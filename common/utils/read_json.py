"""
JSON read function to import json files
"""

import json


def read_json(path):
    """
    Read in a JSON file and return the content as dict

    :param str path: The path to the JSON file
    :return: The file found at the path
    :rtype: dict
    """
    with open(path) as file_opened:
        json_data = json.load(file_opened)
    return json_data
