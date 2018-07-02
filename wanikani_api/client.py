import datetime

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
    Resource)

MISSING = object()


class Client:
    def __init__(self, v2_api_key):
        self.v2_api_key = v2_api_key
        self.url = constants.ROOT
        self.headers = {"Authorization": "Bearer {}".format(v2_api_key)}

    def user_information(self,):
        response = requests.get(self.url + "user", headers=self.headers)
        if response.status_code == 200:
            return UserInformation(response.json())
        elif response.status_code == 401:
            raise InvalidWanikaniApiKeyException(
                "[{}] is not a valid API key!".format(self.v2_api_key)
            )

    def subjects(
        self,
        ids=MISSING,
        types=MISSING,
        slugs=MISSING,
        levels=MISSING,
        hidden=MISSING,
        updated_after=MISSING,
    ):
        response = requests.get(
            self._build_wanikani_api_url("subjects", locals()), headers=self.headers
        )
        return self._serialize_wanikani_response(response)

    def assignments(self):
        response = requests.get(
            self._build_wanikani_api_url("assignments", locals()), headers=self.headers
        )
        return self._serialize_wanikani_response(response)

    def review_statistics(self):
        response = requests.get(
            self._build_wanikani_api_url("review_statistics", locals()),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def study_materials(self):
        response = requests.get(
            self._build_wanikani_api_url("study_materials", locals()),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def summary(self):
        response = requests.get(
            self._build_wanikani_api_url("summary", locals()), headers=self.headers
        )
        return self._serialize_wanikani_response(response)

    def reviews(self):
        response = requests.get(
            self._build_wanikani_api_url("reviews", locals()), headers=self.headers
        )
        return self._serialize_wanikani_response(response)

    def level_progressions(self):
        response = requests.get(
            self._build_wanikani_api_url("level_progressions", locals()),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def resets(self):
        response = requests.get(
            self._build_wanikani_api_url("resets", locals()), headers=self.headers
        )
        return self._serialize_wanikani_response(response)

    def _serialize_wanikani_response(self, response):
        if response.status_code == 200:
            json = response.json()
            type = json["object"]
            if type == "collection":
                return Collection(json)
            else:
                return Resource.factory(json)
        elif response.status_code == 401:
            raise InvalidWanikaniApiKeyException(
                "[{}] is not a valid API key!".format(self.v2_api_key)
            )

    def _build_wanikani_api_url(self, endpoint, parameters=None):
        parameter_string = self._build_query_parameters(parameters)
        return "{0}{1}{2}".format(self.url, endpoint, parameter_string)

    def _parse_parameter(self, parameter):
        key = parameter[0]
        value = parameter[1]
        if value == MISSING or key is "self":
            return None
        if isinstance(value, list):
            return "{}={}".format(key, ",".join(str(elem) for elem in value))
        elif isinstance(value, bool):
            return "{}={}".format(key, str(value).lower())
        elif isinstance(value, datetime.datetime):
            return "{}={}".format(key, value.isoformat())
        else:
            return "{}={}".format(key, str(value))

    def _build_query_parameters(self, parameters):
        if parameters:
            query_parameters = list(map(self._parse_parameter, parameters.items()))
            query_parameters = [qp for qp in query_parameters if qp is not None]
            if query_parameters:
                return "?{}".format("&".join(query_parameters))
        return ""
