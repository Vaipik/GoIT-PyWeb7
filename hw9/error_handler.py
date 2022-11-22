from functools import wraps
import sqlalchemy.exc as sqlexception


def error_handler(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
            return result
        except sqlexception.InvalidRequestError as e:
            print(e)
        except ValueError:
            print("You forget to enter data")
    return wrapper
