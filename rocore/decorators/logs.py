import time
import logging
from logging import Logger
from typing import Optional, Callable
from functools import wraps
from rocore.ids import uuid_generator
from rocore.diagnostics import StopWatch
from inspect import iscoroutinefunction


IdGenerator = Callable[[], str]


default_id_generator = uuid_generator()


def log(logger: Optional[Logger] = None,
        id_generator: Optional[IdGenerator] = None):

    if not id_generator:
        id_generator = lambda: next(default_id_generator)

    def log_decorator(fn):
        nonlocal logger

        if logger is None:
            logger = logging.getLogger(f'fn.{fn.__name__}')

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if id_generator:
                function_call_id = id_generator()
                fn.call_id = function_call_id
            # TODO: support assigning an id to the function execution
            # TODO: support measuring the amount of time it takes for the function to execute
            # TODO: support logging the return value
            # TODO: add a similar decorator to rolog, for asynchronous logging
            # TODO: how to pytest logger?
            # TODO: what messages to use?
            # logger.info(f'Calling {fn.__name__}; call {function_call_id}')
            with StopWatch() as stop_watch:
                try:
                    value = fn(*args, **kwargs)
                except Exception as exc:
                    logger.exception(f'Unhandled exception when executing {fn.__name__}', exc)
                    raise

            logger.info(f'Called {fn.__name__}; elapsed {stop_watch.elapsed_ms}')
            return value

        return wrapper
    return log_decorator
