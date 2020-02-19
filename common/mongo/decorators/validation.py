"""
This module holds all validation decorators
"""

import inspect

from bson import ObjectId

def validate_id(target_parameter):
    """
    This layer is needed to be able to parse an argument into a decorator

    :param string target_parameter: The parameter which should be validated
    """

    def validate_id_inner(func):
        """
        ID validation decorator

        :param func func: The function which shall be validated
        """
        def validate(*args, **kwargs):
            """
            Actual validator function

            :param tuple args: All inserted arguments
            :param Object kwargs: All extra arguments inserted as an object
            """
            # Cast args to list so you can mutate the parameters
            args = list(args)

            # Get the original names of all the parameters
            param_names = inspect.getargspec(func)[0]

            # Find the parameter which should be validated
            position = None
            for i in range(len(param_names)):
                if str(target_parameter) == str(param_names[i]):
                    position = i

            # Cast to ObjectId
            if position is not None:
                arg = args[position]
                
                if type(arg) is str:
                    arg = ObjectId(arg)
                
                args[position] = arg

            # Cast back to tuple
            args = tuple(args)

            return func(*args, **kwargs)

        return validate
    return validate_id_inner
