from fabric import Connection, Config
from invoke import Responder
from invoke.exceptions import UnexpectedExit
from App.ssh_arch import SSHArchDevice

from logging import DEBUG
from Logger import logging_config

CLASS_LOG = logging_config.get_simple_logger("device_manager", DEBUG)

class Bridge():

    def __init__(self, host, port, username, password):
        self.device = SSHArchDevice(host, port, username, password)  # Unbridged
        self.connection = None
        self.responder = None
        self.result = None
        self.stdout = ""
        self.stderr = ""
    
    # Connection
    def _connect_fabric(self):
        target = "{}@{}".format(self.device.username, self.device.host)
        self.connection = Connection(target, connect_kwargs={'password': self.device.password})

    def _connect_fabric_sudo(self):
        target = "{}@{}".format(self.device.username, self.device.host)
        config = Config(overrides={'sudo': {'password': self.device.password}})
        self.connection = Connection(target, connect_kwargs={'password': self.device.password}, config=config)

    def _create_responder(self, su=False):
        if su:
            # Responder with SU credentials
            self.responder = Responder(
                pattern=r'Password:',
                response='{}\n'.format(self.device.root_password),
            )
            return self.responder
        else:
            # responder requires sudo password
            self.responder = Responder(
                pattern=r'\[sudo\] password for *',
                response='{}\n'.format(self.device.password),
            )
            return self.responder
        
    def _result_parser(self):
        if not self.result:
            CLASS_LOG.warning("Result buffer empty. Run a command.")
        else:
            if self.result.stderr:
                self.stderr = self.result.stderr
                CLASS_LOG.warning("Cmd returned error or warning:\n{}".format(self.result.stderr))
                print("Current command yielded stderr:\n{}".format(self.stderr))  #Remove
            if self.result.stdout:
                self.stdout = self.result.stdout
                CLASS_LOG.info("Cmd success returned:\n{}".format(self.result.stdout))
                print("Current command yielded stdout:\n{}".format(self.stdout))  #Remove

    def _command_helper(self, cmd, sudo, responder):
        try:
            if sudo:
                # CLASS_LOG.debug("sudo command")
                if responder:
                    resp = Responder(
                        pattern=r'\[sudo\] password for *',
                        response='{}\n'.format(self.device.password),)
                    self.result = self.connection.sudo(self.device.cmd_format(cmd), pty=True, watchers=[resp])
                else:
                    self.result = self.connection.sudo(self.device.cmd_format(cmd))
            else:
                if responder:
                    resp = self._create_responder()
                    self.result = self.connection.run(self.device.cmd_format(cmd), pty=True, watchers=[resp])
                else:
                    self.result = self.connection.run(self.device.cmd_format(cmd))
            CLASS_LOG.debug("Finished command helper. Obtained result: {}".format(self.result))
        except UnexpectedExit:
            self.stderr = "Unexpected exit probably expecting a responder"
            CLASS_LOG.critical("Unexpected exit probably expecting a responder")
        return self.result

    # command
    def _command(self, cmd, sudo=False, respond=False):
        if not self.connection:
            CLASS_LOG.critical("Must have an active fabric connection.")
            return

        if isinstance(cmd, list):
            for c in cmd:
                self._command_helper(self.device.cmd_format(c), sudo, respond)
                self._result_parser()
        else:
            self._command_helper(self.device.cmd_format(cmd), sudo, respond)
        self._result_parser()

    # Fabric execute
    def execute(self, cmd, sudo=False, respond=False):
        """Creates a fabric connection and sends a command."""
        # Setup connection and set responder
        if sudo:
            self._connect_fabric_sudo()
        else:
            self._connect_fabric()
        CLASS_LOG.info("Created fabric connection")

        # Send command and parse result
        CLASS_LOG.info("Executing command as sudo: {} and responding: {}".format(sudo, respond))
        self._command(cmd, sudo, respond)
        CLASS_LOG.info("Command executed.")

        if not self.result:
            CLASS_LOG.error("Run command first.")
            exit(-1)

        if self.stdout and self.stderr:
            CLASS_LOG.warning("The following warnings were found:\n{}".format(self.stderr))
            CLASS_LOG.info("The following responses were found:\n{}".format(self.stdout))
            return self.stdout

        if self.stdout:
            CLASS_LOG.info("The following responses were found:\n{}".format(self.stdout))
            return self.stdout

        if self.stderr:
            CLASS_LOG.warning("The following warnings were found:\n{}".format(self.stderr))
            return self.stderr

    # SSH (Paramiko) execute
    def execute_ssh_command(self, cmd, time_override=1, su=False):
        """Sends a command(s) using an attached device without fabric."""
        return self.device.send_command(cmd, time_override, su)


def setup_device_example():
    host = "192.168.1.243"
    port = 22
    username = "alarm"
    password = "alarm"
    root_password = "root"
    new_username="raspi"
    new_password="ipsar"

    print("Bridge Fabric-SSH Archlinux Arm default credentials:")
    bridge = Bridge(host, port, username, password)
    bridge.device.add_root_password(root_password)

    print("Set pacman, sudo, and new user")
    bridge.device._set_pacman()
    bridge.device._update_pacman()
    bridge.device._set_sudo()
    bridge.device._set_new_user(new_username, new_password)
    bridge.execute_ssh_command(["sudo -i", "{}".format(new_password)], 2)

    print("Connecting to new user: {}".format(new_username))
    bridge = Bridge(host, port, new_username, new_password)

    bridge.execute("whoami")
    bridge.execute("Pacman -Syu --nocornfirm", sudo=True)