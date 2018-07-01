import requests

from wanikani_api import constants
from wanikani_api.exceptions import InvalidWanikaniApiKeyException
from wanikani_api.models import (
    UserInformation,
    Subject,
    Collection,
    Assignment,
    ReviewStatistic,
    StudyMaterial,
    Summary,
    Review,
    LevelProgression,
    Reset,
)


class Client:
    def __init__(self, v2_api_key):
        self.v2_api_key = v2_api_key
        self.url = constants.ROOT
        self.headers = {"Authorization": "Bearer {}".format(v2_api_key)}

    def user_information(self):
        response = requests.get(self.url + "user", headers=self.headers)
        if response.status_code == 200:
            return UserInformation(response.json())
        elif response.status_code == 401:
            raise InvalidWanikaniApiKeyException(
                "[{}] is not a valid API key!".format(self.v2_api_key)
            )

    def subjects(self):
        response = requests.get(self.url + "subjects", headers=self.headers)
        return self._serialize_wanikani_response(Subject, response)

    def assignments(self):
        response = requests.get(self.url + "assignments", headers=self.headers)
        return self._serialize_wanikani_response(Assignment, response)

    def review_statistics(self):
        response = requests.get(self.url + "review_statistics", headers=self.headers)
        return self._serialize_wanikani_response(ReviewStatistic, response)

    def study_materials(self):
        response = requests.get(self.url + "study_materials", headers=self.headers)
        return self._serialize_wanikani_response(StudyMaterial, response)

    def summary(self):
        response = requests.get(self.url + "summary", headers=self.headers)
        return self._serialize_wanikani_response(Summary, response)

    def reviews(self):
        response = requests.get(self.url + "reviews", headers=self.headers)
        return self._serialize_wanikani_response(Review, response)

    def level_progressions(self):
        response = requests.get(self.url + "level_progressions", headers=self.headers)
        return self._serialize_wanikani_response(LevelProgression, response)

    def resets(self):
        response = requests.get(self.url + "resets", headers=self.headers)
        return self._serialize_wanikani_response(Reset, response)

    def _serialize_wanikani_response(self, cls, response):
        if response.status_code == 200:
            json = response.json()
            type = json["object"]
            if type == "collection":
                return Collection(json, cls)
            elif type == "report":
                return cls(json)
            else:
                return cls.factory(json)
        elif response.status_code == 401:
            raise InvalidWanikaniApiKeyException(
                "[{}] is not a valid API key!".format(self.v2_api_key)
            )
