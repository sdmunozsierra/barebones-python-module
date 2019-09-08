"""Example file containing the main executable for an app."""
from logging import DEBUG
from Logger import logging_config

# Create a Logger for main_app
MAIN_LOG = logging_config.get_simple_logger("main_logger", DEBUG)


# Main program
def __main__():
    MAIN_LOG.info("Running Main Program inside main_app.py")
    MAIN_LOG.info("Using simple_function to add 1 to 1")
    simple_function(1)


# Simple function to be tested
def simple_function(real_number):
    """:returns: real_number + 1"""
    MAIN_LOG.debug("Adding 1 to %d", real_number)
    return real_number + 1
