import threading
import time
from random import randint
import requests.exceptions
import threading

import logging
logger = logging.getLogger(__name__)

class AkhetAgentInstanceRunner(threading.Thread):

    used_ws_vnc_ports_semaphore = None
    used_ws_vnc_ports = []

    @staticmethod
    def get_free_ws_vnc_port(ws_port_range_config):
        port_ws_vnc = None
        while port_ws_vnc == None:
            AkhetAgentInstanceRunner.used_ws_vnc_ports_semaphore.acquire()
            port_ws_vnc = randint(ws_port_range_config['low'],ws_port_range_config['high'])

            if port_ws_vnc in AkhetAgentInstanceRunner.used_ws_vnc_ports:
                port_ws_vnc = None
                time.sleep(1)
            else:
                AkhetAgentInstanceRunner.used_ws_vnc_ports.append(port_ws_vnc)
            AkhetAgentInstanceRunner.used_ws_vnc_ports_semaphore.release()
        logger.debug("Using port {}".format(port_ws_vnc))
        return port_ws_vnc

    @staticmethod
    def free_ws_vnc_port(port_ws_vnc):
        AkhetAgentInstanceRunner.used_ws_vnc_ports_semaphore.acquire()
        AkhetAgentInstanceRunner.used_ws_vnc_ports.remove(port_ws_vnc)
        AkhetAgentInstanceRunner.used_ws_vnc_ports_semaphore.release()
        logger.debug("Port {} is now free".format(port_ws_vnc))
        return True

    def __init__(self, dockerclient, instance, akhet_agent, config):
        super(AkhetAgentInstanceRunner, self).__init__()
        self.dockerclient = dockerclient
        self.instance = instance
        self.akhet_agent = akhet_agent
        self.logger = logging.getLogger(__name__ + "@" + self.instance.get_instance_id())
        self.cuda_config = config['cuda']
        self.ws_port_range_config = config['ws_port_range']

    def run(self):
        port_ws_vnc = None
        self.running = True
        while self.running:
            self.logger.debug("polling..")
            self.instance.poll()

            if self.instance.get_is_assigned():
                self.logger.info("Get VNC ws port")
                port_ws_vnc = AkhetAgentInstanceRunner.get_free_ws_vnc_port(self.ws_port_range_config)

                fw_env = {"whitelist":"HOST:192.168.0.0/24 HOST:172.16.0.0/12 HOST:10.0.0.0/8"}
                #fw_env = {"blacklist":""}
                #fw_env = {}
                instance_env = {}

                instance_env['AKHETBASE_SHARED'] = "0"
                if self.instance.get_is_shared():
                    instance_env['AKHETBASE_SHARED'] = "1"

                instance_env['AKHETBASE_PERSISTENT'] = "0"
                if self.instance.get_is_persistent():
                    instance_env['AKHETBASE_PERSISTENT'] = "1"

                instance_env['AKHETBASE_VNCPASS'] = self.instance.get_vnc_password()

                if self.instance.has_user_config():
                    instance_env['AKHETBASE_USER'] = self.instance.get_username()
                    instance_env['AKHETBASE_USER_LABEL'] = self.instance.get_user_label()
                    instance_env['AKHETBASE_UID'] = self.instance.get_user_id()

                is_privileged = self.instance.get_is_privileged()

                self.logger.info("Create docker for firewall")
                docker_obj_fw = self.dockerclient.containers.create(
                    image="akhet/base/firewall",
                    #command="/bin/sh",
                    name="akhet-instance-" +  self.instance.get_instance_id() + "-fw",
                    hostname= self.instance.get_instance_id(),
                    labels={"akhetfw":"1","akhetid": self.instance.get_instance_id()},
                    environment=fw_env,
                    detach=True,
                    tty=True,
                    privileged=True,
                    ports={"6080/tcp":port_ws_vnc},
                    read_only=True
                )

                devices = []
                volumes = {}

                if self.cuda_config['enabled']:
                    if 'com.nvidia.cuda.version' in self.dockerclient.images.get(self.instance.get_image()).attrs['ContainerConfig']['Labels']:
                        volumes[self.cuda_config['volume']] = {
                            'mode':'ro',
                            'bind':'/usr/local/nvidia',
                        }
                        for device in self.cuda_config['devices']:
                            devices.append(device)

                self.logger.info("Create docker for the user")
                docker_obj = self.dockerclient.containers.create(
                    image= self.instance.get_image(),
                    #command="/bin/sh",
                    name="akhet-instance-" +  self.instance.get_instance_id(),
                    labels={"akhetinstance":"1","akhetid": self.instance.get_instance_id()},
                    environment=instance_env,
                    detach=True,
                    tty=True,
                    privileged=is_privileged,
                    network_mode="container:akhet-instance-" +  self.instance.get_instance_id() + "-fw",
                    devices=devices,
                    volumes=volumes
                )

                self.logger.info("Updateing the status")
                self.instance.set_created(port_ws_vnc)
            elif self.instance.get_is_created():
                count = 0
                for label in ["akhetfw","akhetinstance"]:
                    for docker_container in self.dockerclient.containers.list(all=True,filters={"label":["{}=1".format(label),"akhetid={}".format(self.instance.get_instance_id())]}):
                        count = count + 1
                        self.logger.info("Starting the docker {}".format(docker_container))
                        docker_container.start()
                if count == 2:
                    self.instance.set_ready()
            elif self.instance.get_is_ready():
                total = 0
                running = 0
                for docker_container in self.dockerclient.containers.list(all=True,filters={"label":["akhetid={}".format(self.instance.get_instance_id())]}):
                    total = total + 1
                    if docker_container.status == "running":
                        running = running + 1
                if running == total:
                    self.logger.info("Docker ready")
                    self.instance.set_running()
            elif self.instance.get_is_running():
                total = 0
                running = 0
                for docker_container in self.dockerclient.containers.list(all=True,filters={"label":["akhetid={}".format(self.instance.get_instance_id())]}):
                    total = total + 1
                    if docker_container.status == "running":
                        running = running + 1
                if running < total:
                    self.logger.info("Instance not running")
                    self.instance.set_stopped()
            elif self.instance.get_is_stopped():
                if self.instance.get_is_persistent():
                    self.logger.info("Instance must be persistent. Setting for start")
                    self.instance.set_ready()
                else:
                    for docker_container in self.dockerclient.containers.list(filters={"label":["akhetid={}".format(self.instance.get_instance_id())]}):
                        self.logger.info("Killing {} docker".format(docker_container))
                        docker_container.kill()

                    self.instance.set_deleted()
            elif self.instance.get_is_deleted():
                self.logger.info("Instance ready to be deleted")

                self.running = False
            else:
                self.logger.error("Undefined status for {}".format(self.instance))

            time.sleep(1)

        timeouterror = None
        while (timeouterror == None) or timeouterror:
            timeouterror = None
            for label in ["akhetinstance","akhetfw"]:
                for docker_container in self.dockerclient.containers.list(all=True,filters={"label":["{}=1".format(label),"akhetid={}".format(self.instance.get_instance_id())]}):
                    try:
                        self.logger.info("Stopping {} docker".format(docker_container))
                        docker_container.stop()
                        self.logger.info("Remove {} docker".format(docker_container))
                        docker_container.remove()
                        if timeouterror == None:
                            timeouterror = False
                    except requests.exceptions.Timeout as e:
                        self.logger.info("Timeout exception {} docker".format(docker_container))
                        timeouterror = True

        while not AkhetAgentInstanceRunner.free_ws_vnc_port(port_ws_vnc):
            time.sleep(1)

AkhetAgentInstanceRunner.used_ws_vnc_ports_semaphore = threading.Lock()
