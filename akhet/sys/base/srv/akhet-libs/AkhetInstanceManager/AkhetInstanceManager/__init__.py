import json
import requests
import urllib.parse

from AkhetInstance import AkhetInstance

class AkhetInstanceManager(object):

    def __init__(self, akhet_api_url):
        super(AkhetInstanceManager, self).__init__()
        self.akhet_api_url = akhet_api_url

    def poll(self, images_list):
        #for image_name in images_list:
        if True:
            payload = {}
            payload['status'] = 'pending'
            #payload['image'] = image_name
            url = self.akhet_api_url+"/api/v1/instance?{}".format(
                urllib.parse.urlencode({"where":json.dumps(payload)})
            )
            reply = requests.get(url)
            self.created_pending = []
            for item in reply.json()['_items']:
                if item['image'] in images_list:
                    self.created_pending.append(item)

    def get_pending(self,akhet_agent_obj):
        if len(self.created_pending) > 0:
            pending = self.created_pending[0]
            url = self.akhet_api_url+"/api/v1/instance/{}".format(pending['_id'])
            reply = requests.patch(
                url=url,
                json={"status":"assigned","agent_hostname":akhet_agent_obj.get_hostname()},
                headers={'If-Match': pending['_etag']}
            )
            if reply.status_code == 200:
                del self.created_pending[0]
                return AkhetInstance(self.akhet_api_url, pending['_id'])
        return None

    def get_list_running_isntances(self):
            payload = {}
            payload['status'] = 'running'
            url = self.akhet_api_url+"/api/v1/instance?{}".format(
                urllib.parse.urlencode({"where":json.dumps(payload)})
            )
            reply = requests.get(url)
            ids = []
            for instance in reply.json()['_items']:
                ids.append(instance['_id'])
            return ids
