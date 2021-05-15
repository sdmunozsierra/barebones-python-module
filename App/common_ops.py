"""Common operations to be performed on arch devices."""
from App.device_manager import Bridge

class ArchLinuxArmDevice():
    """This class includes rpi4 64-bits 8GB RAM version."""
    def __init__(self, device, root_password=None):
        self.device = device
        if root_password:
            self.device.add_root_password(root_password)

    def send_command(self, cmd, sudo=False):
        return self.device.execute(cmd, sudo) # responder arg not needed?
    
    def low_level_setup(self, new_username, new_password):
        self.device._set_pacman()
        self.device._update_pacman()
        self.device._set_sudo()
        self.device._set_new_user(new_username, new_password)

    def op_install_sudo(self):
        self.send_command(["pacman -S sudo --noconfirm", "echo $'\n%wheel ALL=(ALL) ALL' >> /etc/sudoers"], sudo= True)
        
    def op_pacman_package_install(self, package, needed=True, noconfirm=True):
        cmd = "pacman -S "
        flags = ""
        if needed:
            flags += " --needed"
        if noconfirm:
            flags += " --noconfirm"

        if isinstance(package, list):
            for p in package:
                self.send_command(cmd + p + flags, sudo=True)
        else:
            command = cmd + package + flags
            print(command)
            self.send_command(cmd + package + flags, sudo=True)

    def op_new_user(self, new_username, new_password):
        command_list = [
        "useradd -m -g users -G wheel -s /bin/bash {}".format(new_username),
        "passwd",
        "{}".format(new_password),
        "{}".format(new_password),
        "echo {} > /etc/hostname".format(new_username),
        "echo 127.0.0.1 localhost {} >> /etc/hosts".format(new_username),
        "usermod -aG docker {}".format(new_username)
        ]
        self.send_command(command_list, sudo=True)

    def op_set_time(self):
        command_list = [
            'echo "LANG=en_US.UTF-8" >> /etc/locale.conf', 
            'echo "LC_COLLATE=C" >> /etc/locale.conf',
            'echo "LC_TIME=en_US.UTF-8" >> /etc/locale.conf'
        ]
        self.send_command(command_list, sudo=True)

    def set_locale(self):
        command_list = [
            "ln -s /usr/share/zoneinfo/America/New_York /etc/localtime", 
            'echo "en_US.UTF-8 UTF-8" > /etc/locale.gen', 
            "locale-gen"]
        self.send_command(command_list, sudo=True)

    def install_yay(self):
        # Install yay needs git
        self.execute("git -c http.sslVerify=false clone https://aur.archlinux.org/yay.git")
        self.execute("cd yay && makepkg -si --noconfirm", respond=True)
        
    def system_setup(device, new_username, new_password):
        if not isinstance(device, Bridge):
            print("Only Bridges")
            exit(-1)

        print("Setting up device: ")
        # Populate Archlinux Arm
        device.execute(["pacman-key --init", "pacman-key --populate archlinuxarm"],
        time_override=10, su=True)

        # Set new users 
        device.execute(["useradd -m -g users -G wheel -s /bin/bash {}".format(new_username),
        "passwd {}".format(new_username), new_password, new_password], 2, True)
        device.execute("echo {} > /etc/hostname".format(new_username), 2, True)
        device.execute("echo 127.0.0.1 localhost {} >> /etc/hosts".format(new_username), 2, True)
        device.execute("usermod -aG docker {}".format(new_username), 2, True)

        # Set Locale
        device.execute([
            "ln -s /usr/share/zoneinfo/America/New_York /etc/localtime", 
            'echo "en_US.UTF-8 UTF-8" > /etc/locale.gen', 
            "locale-gen"], su=True)

        # Set time
        device.execute(["su {}\n".format(new_username), "{}\n".format(new_password)], 2)
        device.execute('echo "LANG=en_US.UTF-8" >> /etc/locale.conf')
        device.execute('echo "LC_COLLATE=C" >> /etc/locale.conf')
        device.execute('echo "LC_TIME=en_US.UTF-8" >> /etc/locale.conf')

        # Install Sudo
        device.execute(["pacman -S sudo --noconfirm", "echo $'\n%wheel ALL=(ALL) ALL' >> /etc/sudoers\n"],
        time_override=10, su=True)

        # Common packages
        # device.execute("pacman -Syu base base-devel git vim docker docker-machine --needed networkmanager --noconfirm\n")
        print("Device setup complete: ")

        

def install_ntp():
    # Install programs using pacman
    # c.sudo("pacman -S ntp --needed --noconfirm\n")
    # c.sudo("ntpd -u ntp:ntp\n")
    # c.sudo("systemctl enable ntpd.service\n")
    # c.run("ntpd -p\n")
    pass