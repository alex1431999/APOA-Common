"""
This module deals with any functionality related to the os environment of the running system
"""

import os

def check_environment(variable_name, default_value):
    """
    Check if an environment variable exists and return its value, if the variable doesn't
    exist, just return the default value

    :param str variable_name: The variable we are looking for
    :param str default_value: The value returned in case the variable does not exist
    """
    return os.environ[variable_name] if variable_name in os.environ else default_value
