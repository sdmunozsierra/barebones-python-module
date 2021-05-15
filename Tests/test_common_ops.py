"""Test common operations or Archlinux devices"""
from App.cluster_manager import Bridge
from App.common_ops import ArchLinuxArmDevice
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

    def test_pacman_package_install(self):
        """Test send a command using fabric."""
        test_bridge = Bridge(host,port,username,password)
        test_bridge.device.add_root_password(root_password)
        test_dev = ArchLinuxArmDevice(test_bridge)

        self.test_dev.op_pacman_package_install("base")
        test_dev.op_pacman_package_install("base-devel")
        test_dev.op_pacman_package_install("git")
        test_dev.op_pacman_package_install(["docker", "docker-machine"])

    def test_common_operations(self):
        """Test common operations on arhc devices."""
        test_bridge = Bridge(host,port,username,password)
        test_bridge.device.add_root_password(root_password)
        test_dev = ArchLinuxArmDevice(test_bridge)


