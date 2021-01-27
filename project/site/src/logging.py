import inspect
import logging.config
import os
import re

import logging_tree


def line_info(definition):
    return (
        f"{inspect.getsourcefile(definition)}:{inspect.getsourcelines(definition)[1]}"
    )


class ConsoleLogFilter(logging.Filter):
    def filter(self, record):
        log_console_filter = os.environ.get("LOG_CONSOLE_FILTER", "")
        containing_module_name = list(
            filter(len, re.split(r"[,\s]", log_console_filter))
        )
        return any(
            [module_name in record.name for module_name in containing_module_name]
        )


def configure_logging():
    """
    1. The module "level" settings does not apply to propagated messages from
       children loggers. This means you can have DEBUG in a child and WARNING in
       parent, and the DEBUG log is still printed.
    2. When setting "handlers" on a module, the log is handled by the handlers
       as well as being propagated to parents (when propagate is True).
    3. propagte is True by default
    """
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "ConsoleLogFilter": {
                "()": "src.logging.ConsoleLogFilter",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "level": os.environ.get("LOG_CONSOLE_LEVEL", "INFO"),
                "filters": ["ConsoleLogFilter"],
            },
        },
        "formatters": {
            "verbose": {
                "format": "{asctime} - {name} {funcName}(..) {levelname} - {message}",
                "style": "{",
            },
            "console": {
                "format": "{asctime} - {name} {funcName}(..) {levelname} - {message}",
                "style": "{",
            },
        },
        "loggers": {
            "": {"handlers": ["console"]},
            "django": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "src": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "tests": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        },
    }

    logging.config.dictConfig(LOGGING)
    return LOGGING


def debug():
    logging_tree.printout()
