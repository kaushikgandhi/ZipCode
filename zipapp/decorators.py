
from functools import wraps

from rest_framework.exceptions import APIException



class BadRequest(APIException):
    '''
        Raises the bad request exception if the incoming data coming from client
        is not valid.
    '''
    status_code = 400
    default_detail = "The request isn't valid."



def require_params(*required_params):
    '''
        A decorator to make sure required query parameters are passed for the request.
        This decorator could be used with API Views that accept first argument as request.
        If the required parameters are missing, BadRequest is raised.
    '''
    def decorator(func):
        '''
            Decorator to wrap the func.
        '''
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            '''
                First checks if all the required parameters are present in the request.
                If so, function is called with the parameters. If not, BadRequest is raised.
            '''
            # Make sure we have all the required parameters passed in.
            for param in required_params:
                if (param not in request.GET) and (param not in request.POST):
                    raise BadRequest('Parameter: %s is required.' % (param))

            # If everything looks correct, lets just proceed with view execution.
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator

