import sys
import os
from dotenv import load_dotenv
from App.device_manager import Bridge
from App.common_ops import ArchLinuxArmDevice
from Logger.logging_config import get_simple_logger
CLASS_LOG = get_simple_logger("exec_in_target")  # Defaults as DEBUG

load_dotenv()
host_list = os.getenv("HOST_LIST")
host_list = host_list.split(",")
port = os.getenv("PORT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
root_password = os.getenv("ROOT_PASSWORD")
new_username = os.getenv("NEW_USERNAME")
new_password = os.getenv("NEW_PASSWORD")
swarm_token = os.getenv("SWARM_TOKEN")
swarm_leader = os.getenv("SWARM_LEADER")

def exec_in_all():
    print(host_list)

    message = "Executing in the following hosts: {}".format(host_list)
    print(message)
    CLASS_LOG.info(message)
    
    if not isinstance(host_list, list):
        message = "Only list of hosts"
        print(message)
        CLASS_LOG.critical(message)
        sys.exit()

    # for i in range(len(host_list)):
    #     bridge = Bridge(host_list[i], port, username, password)
    #     dev = ArchLinuxArmDevice(bridge, root_password)
    #     message = "Creating bridge with user {} at {}".format(username, host_list[i])
    #     print(message)
    #     CLASS_LOG.info(message)


    #     hostname = "rpi64{}".format(i)
    #     message = "Setting up new device "
    #     print(message)
    #     CLASS_LOG.info(message)
    #     dev.new_system_setup(new_username, new_password, hostname)

    for i in range(len(host_list)):
        bridge = Bridge(host_list[i], port, new_username, new_password)
        dev = ArchLinuxArmDevice(bridge, root_password)

        message = "Creating bridge with user {} at {}".format(new_username, host_list[i])
        print(message)
        CLASS_LOG.info(message)

        # dev.docker_setup()
        message = "Joining docker swarm user {} at {}".format(new_username, swarm_leader)
        print(message)
        CLASS_LOG.info(message)
        dev.op_set_datetime()
        dev.docker_swarm_join(swarm_token, swarm_leader)


def exec_target(target_num):
    bridge = Bridge(host_list[target_num], port, new_username, new_password)
    dev = ArchLinuxArmDevice(bridge, root_password)
    result = dev.op_set_datetime()
    print(result)
    dev.send_command("whoami")
    dev.send_command("date")

