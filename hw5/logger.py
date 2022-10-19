from functools import partial, wraps
import logging
from time import time


def logged(func=None, *_, level=logging.DEBUG, name=None, message=None):

    if func is None:
        return partial(logged, level=level, name=name, message=message)

    log_name = name if name else func.__name__
    log_format = '%(asctime)s [%(levelname)s] %(processName)s %(lineno)s %(message)s'
    logger = logging.getLogger(log_name)
    logging.basicConfig(
        level=level,
        format=log_format
    )

    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time()
        try:
            result = func(*args, **kwargs)
            log_message = f"done in {time() - start_time}"
            log_message = message + ' ' + log_message if message else log_message
            logger.log(level=level, msg=log_message)
            return result
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))

    return wrapper


def extra_loger(name: str):

    log_format = '%(asctime)s [%(levelname)s] %(processName)s %(message)s'
    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

    return logger

