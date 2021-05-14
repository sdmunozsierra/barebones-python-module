"""Simple test file for ssh_arch.py."""
from App.ssh_arch import SSHArchDevice
from unittest import TestCase

# Create a logger if needed for testing cases
from Logger.logging_config import get_simple_logger
TEST_LOG = get_simple_logger("test_ssh_arch.py")  # Defaults as DEBUG

# These should come from env settings
host = "192.168.1.2"
port = 22
username = "alarm"
password = "alarm"
root_password = "root"
# ssh = None
# channel = None
# data = None

# class RunConnectionTests(TestCase):

#     def test_connect_ssh(self):
#         """Tests the main function of connecting through SSH."""
#         TEST_LOG.info("SSH connection")
#         test_dev = SSHArchDevice(host, port, username, password)

#         test_dev._connect_ssh()

#         self.assertIsNotNone(test_dev.ssh)

#     def test_close_ssh(self):
#         """Tests the main function of connecting through SSH."""
#         TEST_LOG.info("SSH connection close connection")
#         test_dev = SSHArchDevice(host, port, username, password)
#         test_dev._connect_ssh()

#         test_dev._close_ssh()

#         self.assertIsNone(test_dev.ssh)

#     def test_connect_channel(self):
#         """Tests the main function of connecting through SSH."""
#         TEST_LOG.info("SSH channel connection")
#         test_dev = SSHArchDevice(host, port, username, password)
#         test_dev._connect_ssh()

#         test_dev._connect_channel()

#         self.assertIsNotNone(test_dev.channel)

#     def test_close_channel(self):
#         """Tests the main function of connecting through SSH."""
#         TEST_LOG.info("SSH channel close connection")
#         test_dev = SSHArchDevice(host, port, username, password)
#         test_dev._connect_ssh()
#         test_dev._connect_channel()

#         test_dev._close_channel()

#         self.assertIsNone(test_dev.channel)
    
#     def test_bind_unbind(self):
#         """Tests the main function of connecting through SSH."""
#         TEST_LOG.info("SSH channel close connection")
#         test_dev = SSHArchDevice(host, port, username, password)

#         self.assertIsNone(test_dev.ssh)
#         self.assertIsNone(test_dev.channel)

#         test_dev.bind()
#         self.assertIsNotNone(test_dev.ssh)
#         self.assertIsNotNone(test_dev.channel)

#         test_dev.unbind()
#         self.assertIsNone(test_dev.ssh)
#         self.assertIsNone(test_dev.channel)

class RunSshTests(TestCase):

    def test_execute(self):
        """Test send a command."""
        test_dev = SSHArchDevice(host, port, username, password)
        res = test_dev.execute("whoami")
        self.assertIn("alarm", res)

        test_dev.add_root_password('root')
        res = test_dev.execute("whoami", su=True)
        self.assertIn("root", res)
        
    def test_execute_list(self):
        """Test send a command."""
        test_dev = SSHArchDevice(host, port, username, password)
        res = test_dev.execute(["uname -a", "whoami", "free -hg"])
        self.assertIn("GNU/Linux", res)

        test_dev.add_root_password('root')
        res = test_dev.execute(["uname -a", "whoami", "free -hg"], su=True)
        self.assertIn("GNU/Linux", res)


