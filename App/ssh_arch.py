"""Execute commands in a device running ssh. Compatible with Raspberry Pi 4 running on arch linux arm."""
import sys
import time
import paramiko
from socket import timeout, gaierror
from paramiko.channel import Channel
from paramiko.ssh_exception import AuthenticationException, SSHException

from logging import DEBUG
from Logger import logging_config

CLASS_LOG = logging_config.get_simple_logger("ssh_arch", DEBUG)

class SSHArchDevice():

    def __init__(self, host, port, username, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.root_password = None
        self.ssh = None
        self.channel = None
        self.data_output = None
        self.binded = False

    # Connection methods
    def _connect_ssh(self):
        if self.ssh:
            CLASS_LOG.warning("SSH connection established already: {}".format(self.host))
            return
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, self. port, self.username, self.password)
            CLASS_LOG.debug("Connected to device using SSH")
        except (timeout, AuthenticationException, gaierror):
            CLASS_LOG.critical("Could not connect to host {} on port {}".format(self.host))
            sys.exit()

    def _close_ssh(self):
        if not self.ssh:
            CLASS_LOG.warning("SSH connection already closed: {}".format(self.host))
            return
        try:
            self.ssh.close()
            self.ssh = None
            CLASS_LOG.debug("Closed SSH connection")
        except:
            CLASS_LOG.warning("Could not close ssh connection: {}".format(self.host))

    def _connect_channel(self):
        if not self.ssh:
            CLASS_LOG.warning("Create ssh connection first: {}".format(self.host))
            return
        if self.channel:
            CLASS_LOG.warning("SSH channel connection established already: {}".format(self.host))
            return
        try:
            self.channel:Channel = self.ssh.invoke_shell()
            self.binded = True
        except (SSHException):
            CLASS_LOG.critical("Failed to invoke a sheel in host: {}".format(self.host))
            sys.exit()

    def _close_channel(self):
        if not self.channel:
            CLASS_LOG.warning("Create channel ssh connection first: {}".format(self.host))
            return
        try:
            self.channel.close()
            self.channel = None
            self.binded = False
            CLASS_LOG.debug("Closed channel connection")
        except:
            CLASS_LOG.warning("Could not close channel for host: {}".format(self.host))

    # Public connection methods
    def bind(self):
        self._connect_ssh()
        self._connect_channel()
        self.binded = True
        CLASS_LOG.debug("Binded")

    def unbind(self):
        self._close_channel()
        self._close_ssh()
        self.binded = False
        CLASS_LOG.debug("Unbinded")

    # Formatter
    def cmd_format(self, command):
        """Format a command putting a new line.
        Set as public as this can be overwritten.
        """
        if isinstance(command, list):
            CLASS_LOG.error("Only Single commands are accepted. ")
            return
        return("{}\n".format(command))

    # Channel
    def _command_channel_sender(self, parsed_command):
        """Use an active channel to send a parsed command."""
        self.channel.send(parsed_command)

    def _command_channel_receiver(self, bytes=1024):
        """Receives the data and appends to data_output."""
        if not self.data_output:
            self.data_output = ""
        self.data_output += self.channel.recv(bytes).decode()
        return self.data_output

    # Command
    def _command(self, cmd, wait=1):
        """Sends a command using an activce channel and then waits and recevices data"""
        if not self.binded:
            CLASS_LOG.critical("Must have an active channel first")
            return

        if isinstance(cmd, list):
            for c in cmd:
                self._command_channel_sender(self.cmd_format(c))
                time.sleep(wait)
            self._command_channel_receiver()
        else:
            # Normal Command # Permissionless
            self._command_channel_sender(self.cmd_format(cmd)) 
            time.sleep(wait)
            self._command_channel_receiver()
        return self.data_output

    def _su_command(self, command, wait=1):
        """Command can be a list and will send each command without clossing the channel until the end."""
        if not self.root_password:
            CLASS_LOG.critical("Must have an root password first")
            return
        
        data_output = ""
        data_output += self._command("su -") # Start su session

        # Wait for command to finish
        data_output += self._command(self.root_password)  # Send the root password
        # Wait for command to finish
        data_output += self._command(command) # Send expected command as su
        # Wait for command to finish
        data_output += self._command("exit")  # Close su session
        # receive output
        CLASS_LOG.info("SU Command ran")
        return data_output

    def send_command(self, command, time_override, su=False):
        output = ""
        if su:
            CLASS_LOG.info("Sending a su command through SSH")
            output += self._su_command(command, time_override)
        else:
            CLASS_LOG.info("Sending a command through SSH")
            output += self._command(command, time_override)

        return output
    
    # Add root password to class
    def add_root_password(self, root_password):
        self.root_password = root_password

    # High level execute a command
    def execute(self, command=None, time_override=5, su=False):
        self.bind()
        if self.data_output:  # Empty buffer
            self.data_output = ""
        if not command:
            CLASS_LOG.error("Command argument not present")
            return
        CLASS_LOG.info("Host: {}\nExecute in {} seconds: {}".format(self.host, time_override, command))
        response = self.send_command(command, time_override, su)
        CLASS_LOG.info("SSH Response:\n{}".format(response))
        self.unbind()
        return response

    # Low level instructions to be able to use instead of Fabric
    def _set_pacman(self):
        self.execute("pacman-key --init", su=True)
        self.execute("pacman-key --populate archlinuxarm", su=True)

    def _update_pacman(self):
        self.execute("pacman -Syu --noconfirm", time_override=360, su=True)

    def _set_sudo(self):
        self.execute("pacman -S sudo --noconfirm", time_override=10, su=True)
        self.execute("echo $'\n%wheel ALL=(ALL) ALL' >> /etc/sudoers", su=True)

    def _set_new_user(self, new_user, new_password):
        self.execute([
            "passwd {}".format(new_user),  # Change password
            "{}".format(new_password),     # First password
            "{}".format(new_password)],    # Confirm password
            2, su=True)
        self.execute("useradd -m -g users -G wheel -s /bin/bash {}".format(new_user), 2, su=True)
