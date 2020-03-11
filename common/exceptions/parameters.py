import inspect

class InvalidParameterError(Exception):
    def __init__(self, parameter):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        parameter_name = [var_name for var_name, var_val in callers_local_vars if var_val is parameter][0]
        message = f'Invallid value: "{parameter}" for parameter: "{parameter_name}"'
        super(InvalidParameterError, self).__init__(message)
        
class UnsupportedLanguageError(Exception):
    def __init__(self, language):
        message = f'Unsupported Language: "{language}"'
        super(UnsupportedLanguageError, self).__init__(message)
