"""
This module provides functioanlity to log output to a file within a directory
"""

import os

from datetime import date, datetime

from common.utils.log_types import LogTypes

class Logger():
    """
    This class defines where to log files to and provides
    the functionality to log messages
    """
    def __init__(self, log_folder='./logs'):
        self.log_folder = log_folder

    def log(self, text, log_type='DEBUG', exception=None):
        """
        Log messages, only errors in production

        :param str text: The text that should be logged
        :param str log_type: The type of log message that is being parsed
        :param ex exception: The execption that might have accured during the log
        """
        valid_log_types = [e.value for e in LogTypes]
        if (log_type not in valid_log_types):
            raise ValueError('Invalid log_type "{}", must be either {}'.format(log_type, valid_log_types))

        log_message = text

        if (exception):
            log_message += ", Failed with Exception: {}".format(str(exception))

        # Prepend date to log
        log_message = "[{}][{}] ".format(log_type ,datetime.now()) + log_message

        print(log_message) # Always print the log message to the console

        log_message += "\n" # Make sure you always add a line before you write to a file

        env = os.environ['PYTHON_ENV']

        # Open log file
        today = date.today()
        log_file_path = r"{}/log_{}_{}_{}.txt".format(self.log_folder, today.year, today.month, today.day)
        log_file = open(log_file_path, "a")

        # Only write to log file if the enviroment and log type agree
        if (env == 'DEVELOPMENT' or (env == 'PRODUCTION' and log_type == 'ERROR') or env is None): 
            log_file.write(log_message)

        # Close log file and return
        return log_file.close()
      