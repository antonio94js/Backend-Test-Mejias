import os
from datetime import date, datetime
from rest_framework.exceptions import ValidationError


def on_time(method):
    """[Decorates any model method to assert that none operation is performed out of time]

    Arguments:
        method {[function]} -- [the method to be decorated]
    """
    def validate_limit_hour(*arg, **kwargs):
        today = date.today()
        limit_hour = int(os.environ.get('LIMIT_ORDER_HOUR'))
        limit_datetime = datetime(
            today.year, today.month, today.day, limit_hour)
        
        if datetime.now() > limit_datetime:
            raise ValidationError(
                {'detail': 'The limit hour to place an order for this menu has finished, better luck next time'})
        
        return method(*arg, **kwargs)

    return validate_limit_hour

# Decorator Factory
def throwable(Exception: Exception, message: str, evalute: bool = True):
    """[Wraps up the common behavior when a function needs to return True, False or an Exception in order to avoid code duplication]

    Arguments:
        Exception {Exception} -- [The Exception which needs to be returned only if apply]
        message {str} -- [The message applied when the Exception was raised]

    Keyword Arguments:
        evalute {bool} -- [Sets which boolean value raises the exception, if False the exception will raise only if the function returns False] (default: {True})
    """
    def decorator(func):
        def evaluate_result(*args, **kwargs):
            result = func(*args, **kwargs)
            raise_exception = kwargs.get("raise_exception", True)
            
            if (result == evalute) and raise_exception:
                raise Exception(message)
            
            return result
        return evaluate_result
    return decorator
