"""
This module holds all validation decorators
"""

import inspect

from bson import ObjectId


def validate_id(target_parameters: any):
    """
    This layer is needed to be able to parse an argument into a decorator

    target_parameters can be a string or a list, it will always be converted to a list
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
            param_names = inspect.getfullargspec(func)[0]

            # Make sure the target parameters is a list
            target_parameters_validated = (
                [target_parameters]
                if type(target_parameters) is str
                else target_parameters
            )

            # parse
            for target_parameter in target_parameters_validated:
                arg_parsed, position = parse_parameter(
                    target_parameter, param_names, args, ObjectId
                )

                if arg_parsed:
                    args[position] = arg_parsed

            # Cast back to tuple
            args = tuple(args)

            return func(*args, **kwargs)

        return validate

    return validate_id_inner


def parse_parameter(
    target_parameter: str, param_names: list, args: list, TargetType: any
) -> any:
    # Find the parameter which should be validated
    position = None
    for i in range(len(param_names)):
        if str(target_parameter) == str(param_names[i]):
            position = i

    # Cast to ObjectId
    arg = None
    if position is not None:
        arg = args[position]

        if type(arg) is not TargetType:
            arg = TargetType(arg)

    return arg, position
