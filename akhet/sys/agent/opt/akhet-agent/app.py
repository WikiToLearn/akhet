import time
import docker
import socket
import yaml

from AkhetInstanceManager import AkhetInstanceManager
from AkhetInstance import AkhetInstance
from AkhetAgent import AkhetAgent
from AkhetAgentInstanceRunner import AkhetAgentInstanceRunner

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Getting docker from env...")
dockerclient = docker.from_env()

config_stream = open("/etc/akhet-agent.yml", "r")
config = yaml.load(config_stream)
config_stream.close()

cuda_config = config['cuda']

akhet_api_base = str(config['api_protocol'])
akhet_api_base = akhet_api_base + "://"
akhet_api_base = akhet_api_base + str(config['api_username'])
akhet_api_base = akhet_api_base + ":"
akhet_api_base = akhet_api_base + str(config['api_password'])
akhet_api_base = akhet_api_base + "@"
akhet_api_base = akhet_api_base + str(config['api_host'])
akhet_api_base = akhet_api_base + ":"
akhet_api_base = akhet_api_base + str(config['api_port'])

logger.info("Getting Akhet agent with {} API host...".format(akhet_api_base))
this_hostname = socket.gethostname()
if 'this_hostname' in config:
    this_hostname = config['this_hostname']
if 'use_ip_as_hostname' in config and config['use_ip_as_hostname']:
    this_hostname = socket.gethostbyname(this_hostname)
akhet_agent = AkhetAgent(akhet_api_base, this_hostname)

logger.info("Getting Akhet instance manager with {} API host...".format(akhet_api_base))
akhet_instance_manager = AkhetInstanceManager(akhet_api_base)

logger.info("run...")
running = True
while running:
    logger.debug("agent poll")
    akhet_agent.poll()
    logger.debug("check if this agent is online")
    is_online = akhet_agent.me_is_online()
    if is_online:
        images_list = []
        for image in dockerclient.images.list():
            labels = image.attrs['ContainerConfig']['Labels']
            if labels != None and 'akhetimage' in labels and labels['akhetimage']:
                repo_tags = image.attrs['RepoTags']
                for tag in repo_tags:
                    images_list.append(tag)
        logger.debug("update agent image list")
        akhet_agent.set_images_list(images_list)

        logger.debug("instance manager poll")
        akhet_instance_manager.poll(images_list)

        more_instances = True
        while more_instances:
            instance = akhet_instance_manager.get_pending(akhet_agent)
            logger.debug("Instance: {}".format(instance))
            if instance != None:
                runner = AkhetAgentInstanceRunner(dockerclient, instance, akhet_agent, cuda_config)
                runner.start()
            else:
                more_instances = False
    else:
        print("IS NOT ONLINE")
    time.sleep(1)
