"""Simple test file for main_app.py."""
from App import main_app
from Logger.logging_config import get_simple_logger

# Create a logger if needed for testing cases
TEST_LOG = get_simple_logger("test_log")  # Defaults as DEBUG


def test_simple_function():
    """Tests simple function from main_app.py."""
    TEST_LOG.info("Testing simple_function")
    assert main_app.simple_function(1) == 2
