import requests

class AkhetInstance(object):

    def __init__(self, akhet_api_url, akhet_instance_id):
        super(AkhetInstance, self).__init__()
        self.akhet_api_url = akhet_api_url
        self.akhet_instance_id = akhet_instance_id

    def get_is_pending(self):
        return self.this_instance['status'] == 'pending'

    def get_is_assigned(self):
        return self.this_instance['status'] == 'assigned'

    def get_is_created(self):
        return self.this_instance['status'] == 'created'

    def get_is_ready(self):
        return self.this_instance['status'] == 'ready'

    def get_is_running(self):
        return self.this_instance['status'] == 'running'

    def get_is_stopped(self):
        return self.this_instance['status'] == 'stopped'

    def get_is_deleted(self):
        return self.this_instance['status'] == 'deleted'

    def has_user_config(self):
        return 'user' in self.this_instance

    def get_username(self):
        try:
            return self.this_instance['user']['username']
        except Exception as e:
            return "akhet"

    def get_user_label(self):
        try:
            return self.this_instance['user']['user_label']
        except Exception as e:
            return "Akhet"

    def get_user_id(self):
        try:
            return self.this_instance['user']['user_id']
        except Exception as e:
            return 1000

    def set_pending(self):
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.get_instance_id())
        reply = requests.patch(
            url=url,
            json={"status":"pending"},
            headers={'If-Match': self.get_etag()}
        )
        if reply.status_code == 200:
            self.poll()
        else:
            raise ValueError("Response {}".format(reply.status_code))

    def set_assigned(self):
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.get_instance_id())
        reply = requests.patch(
            url=url,
            json={"status":"assigned"},
            headers={'If-Match': self.get_etag()}
        )
        if reply.status_code == 200:
            self.poll()
        else:
            raise ValueError("Response {}".format(reply.status_code))

    def set_created(self,port_ws_vnc):
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.get_instance_id())
        reply = requests.patch(
            url=url,
            json={
                "status":"created",
                "port_ws_vnc":port_ws_vnc
            },
            headers={'If-Match': self.get_etag()}
        )
        if reply.status_code == 200:
            self.poll()
        else:
            raise ValueError("Response {}".format(reply.status_code))

    def set_ready(self):
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.get_instance_id())
        reply = requests.patch(
            url=url,
            json={"status":"ready"},
            headers={'If-Match': self.get_etag()}
        )
        if reply.status_code == 200:
            self.poll()
        else:
            raise ValueError("Response {}".format(reply.status_code))

    def set_running(self):
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.get_instance_id())
        reply = requests.patch(
            url=url,
            json={"status":"running"},
            headers={'If-Match': self.get_etag()}
        )
        if reply.status_code == 200:
            self.poll()
        else:
            raise ValueError("Response {}".format(reply.status_code))

    def set_stopped(self):
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.get_instance_id())
        reply = requests.patch(
            url=url,
            json={"status":"stopped"},
            headers={'If-Match': self.get_etag()}
        )
        if reply.status_code == 200:
            self.poll()
        else:
            raise ValueError("Response {}".format(reply.status_code))

    def set_deleted(self):
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.get_instance_id())
        reply = requests.patch(
            url=url,
            json={"status":"deleted"},
            headers={'If-Match': self.get_etag()}
        )
        if reply.status_code == 200:
            self.poll()
        else:
            raise ValueError("Response {}".format(reply.status_code))

    def get_instance_id(self):
        return self.akhet_instance_id

    def poll(self):
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.akhet_instance_id)
        self.this_instance = requests.get(url).json()

    def get_etag(self):
        return self.this_instance['_etag']

    def get_is_shared(self):
        if 'shared' in self.this_instance:
            return self.this_instance['shared']
        return False

    def get_is_persistent(self):
        if 'persistent' in self.this_instance:
            return self.this_instance['persistent']
        return False

    def get_is_privileged(self):
        if 'privileged' in self.this_instance:
            return self.this_instance['privileged']
        return False

    def get_vnc_password(self):
        if 'vnc_password' in self.this_instance:
            return self.this_instance['vnc_password']
        return None

    def get_image(self):
        if 'image' in self.this_instance:
            return self.this_instance['image']
        return None

    def get_agent_hostname(self):
        if 'agent_hostname' in self.this_instance:
            return self.this_instance['agent_hostname']
        return None

    def get_port_ws_vnc(self):
        if 'port_ws_vnc' in self.this_instance:
            return self.this_instance['port_ws_vnc']
        return None

    def get_proxies_hostnames(self):
        if 'proxies_hostnames' in self.this_instance:
            return self.this_instance['proxies_hostnames']
        return None

    def add_proxy_hostname(self, proxy_hostname):
        proxies_hostnames = self.get_proxies_hostnames()
        proxies_hostnames.append(proxy_hostname)
        url = self.akhet_api_url+"/api/v1/instance/{}".format(self.get_instance_id())
        reply = requests.patch(
            url=url,
            json={"proxies_hostnames":proxies_hostnames},
            headers={'If-Match': self.get_etag()}
        )
        if reply.status_code == 200:
            self.poll()
        else:
            raise ValueError("Response {}".format(reply.status_code))
