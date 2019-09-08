"""Configuration file for logging."""
import os
import time
import logging
import logging.handlers as handlers
from logging.config import dictConfig
from module_config import ROOT_DIR


def get_log_level(log_level):
    """Return a log level dictionary for set_logger function.
    Return:
        List: Level Name, Integer Constant
    """
    if log_level is logging.DEBUG:
        log_level = ['DEBUG', logging.DEBUG]
    if log_level is logging.INFO:
        log_level = ['INFO', logging.INFO]
    if log_level is logging.WARNING:
        log_level = ['WARNING', logging.WARNING]
    if log_level is logging.ERROR:
        log_level = ['ERROR', logging.ERROR]
    if log_level is logging.CRITICAL:
        log_level = ['CRITICAL', logging.CRITICAL]
    return log_level


def configure_logger(log_level, log_name):
    """Creates a configuration for a logger.
    :param log_level: level of the logger.
    :param log_name: name of the logger.
    :returns: logger.
    """
    dictConfig({
        'version': 1,
        'formatters': {
            'simple': {'format': '%(asctime)s %(levelname)s ' +
                                 ' [%(module)s -> {}] '.format(log_name) +
                                 '  %(message)s',
                       'datefmt': '%H:%M:%S'},
            'default': {
                'format': '%(asctime)s {} %(levelname)s '.format(log_name) +
                          '[%(module)s - Line: %(lineno)d]  ' +
                          '%(message)s'}
        },
        'handlers': {
            'console': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': log_level,
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': 'loggr/{}.log'.format(log_name),
                'maxBytes': 1024,
                'backupCount': 1
            }
        },
        'loggers': {
            log_name: {
                'level': log_level,
                'handlers': ['console', 'file']
            }
        },
        'disable_existing_loggers': False
    })
    return logging.getLogger(log_name)


# Create two loggers to be used across the app
# flasklog = configure_logger(l_lvl, "flasklog")
# phplog = configure_logger(l_lvl, "phplog")

# Create a simple logger in default directory "/Logger"
def get_simple_logger(log_name, log_level=logging.DEBUG):
    """Create a simple logger in the default directory."""
    # Create Logger with name and level
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    # Define a formatter for the Logger
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set path of the logger using ROOT_DIR and log_name
    path = f"{ROOT_DIR}/Logger/{log_name}.log"
    print(f"Using {path} as Logger directory")

    # Set the and formatter and fileHandler
    fileh = logging.FileHandler(path, 'a')
    fileh.setFormatter(formatter)
    logger.addHandler(fileh)

    return logger  # Return Logger
