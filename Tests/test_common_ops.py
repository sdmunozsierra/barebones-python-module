"""Test common operations or Archlinux devices"""
import os
from unittest import TestCase
from Logger.logging_config import get_simple_logger
TEST_LOG = get_simple_logger("test")  # Defaults as DEBUG
from dotenv import load_dotenv

from App.device_manager import Bridge
from App.common_ops import ArchLinuxArmDevice

# These come from env settings
load_dotenv()
host = os.getenv("HOST")
port = os.getenv("PORT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
root_password = os.getenv("ROOT_PASSWORD")

new_username = "newuser"
new_password = "password"

class RunTests(TestCase):

    def test_pacman_package_install(self):
        """Test send a command using fabric."""
        test_bridge = Bridge(host,port,username,password)
        test_dev = ArchLinuxArmDevice(test_bridge, root_password)
        
        test_dev.pacman_install("base")

    # def test_new_user(self):
    #     """New user should be up login."""
    #     test_bridge = Bridge(host,port,username,password)
    #     test_dev = ArchLinuxArmDevice(test_bridge, root_password)

    #     # Create new user
    #     test_dev.op_set_new_user(new_username, new_password)

    #     # New user should be up login.
    #     test_bridge = Bridge(host,port,new_username,new_password)
    #     test_dev = ArchLinuxArmDevice(test_bridge, root_password)

    #     self.assertEqual(test_dev.send_command("whoami"), "newuser\n")

    # def test_yay_isntall(self):
    #     """Test yay install on new user."""
    #     # New user should be up login.
    #     test_bridge = Bridge(host,port,new_username,new_password)
    #     test_dev = ArchLinuxArmDevice(test_bridge, root_password)
    #     test_dev.pacman_install("git")  # depends on

    #     # This test will fail with other versions this is temporary
    #     self.assertIn(test_dev.install_yay(), "yay v10.2.2 - libalpm v12.0.2\n")

    # def test_is_installed(self):
    #     """Test that a program is intalled using pacman."""
    #     # New user should be up login.
    #     test_bridge = Bridge(host,port,new_username,new_password)
    #     test_dev = ArchLinuxArmDevice(test_bridge, root_password)
    #     # result = test_dev.pacman_is_installed("yay")
    #     # self.assertIn("local/yay", result)

    #     result = test_dev.is_package_installed("pikachu")
    #     self.assertIn("local/yay", result)


    # def test_common_operations(self):
    #     """Test common operations on arhc devices."""
