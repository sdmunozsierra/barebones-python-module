"""Configuration file for logging."""
import logging
from module_config import ROOT_DIR


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
