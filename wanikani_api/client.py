import requests

from wanikani_api import constants


class Client:
    def __init__(self, v2_api_key):
        self.v2_api_key = v2_api_key
        self.url = constants.ROOT
        self.headers = {"Authorization": "Bearer {}".format(v2_api_key)}

    def user_information(self):
        return requests.get(self.url + "user", headers=self.headers)

