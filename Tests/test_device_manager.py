"""Simple test file for ssh_arch.py."""
from App.device_manager import Bridge
from unittest import TestCase

# Create a logger if needed for testing cases
from Logger.logging_config import get_simple_logger
TEST_LOG = get_simple_logger("test")  # Defaults as DEBUG

# These should come from env settings
host = "192.168.1.2"
port = 22
username = "alarm"
password = "alarm"
root_password = "root"
ssh = None
channel = None
data = None

class RunTests(TestCase):

    def test_execute(self):
        """Test send a command using fabric."""
        test_dev = Bridge(host,port,username,password)
        test_dev.device.add_root_password('root')

        # Test sudo auto responder as long as add_root_password() is called.
        res = test_dev.execute("whoami", sudo=True)
        self.assertIn("root", res)

    def test_pacman_update(self):
        test_dev = Bridge(host,port,username,password)
        test_dev.device.add_root_password('root')
        res = test_dev.execute("pacman -Syu", sudo=True)
        self.assertIn("full system upgrade", res)