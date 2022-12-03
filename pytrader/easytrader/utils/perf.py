# coding:utf-8
import functools
import logging
import timeit

from easytrader import logger

try:
    from time import process_time
except:
    from time import clock as process_time


def perf_clock(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not logger.isEnabledFor(logging.DEBUG):
            return f(*args, **kwargs)

        ts = timeit.default_timer()
        cs = process_time()
        ex = None
        result = None

        try:
            result = f(*args, **kwargs)
        except Exception as ex1:
            ex = ex1

        te = timeit.default_timer()
        ce = process_time()
        logger.debug(
            "%r consume %2.4f sec, cpu %2.4f sec. args %s, extra args %s"
            % (
                f.__name__,
                te - ts,
                ce - cs,
                args[1:],
                kwargs,
            )
        )
        if ex is not None:
            raise ex
        return result

    return wrapper
