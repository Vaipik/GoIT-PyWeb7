from functools import partial, wraps
import logging
from time import time, sleep


def logged(func=None, *_, level=logging.DEBUG, name: str = None):
    if func is None:
        return partial(logged, level=level, name=name)

    log_name = name if name else func.__module__
    log_format = f'%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s'

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
        except Exception as e:
            logger.log(level=logging.ERROR, msg=e)
        else:
            log_message = f"{func.__name__} done in {time() - start_time}"
            logger.log(level, log_message)
            return result

    return wrapper
