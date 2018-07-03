import requests

from wanikani_api import constants, models
from wanikani_api.exceptions import InvalidWanikaniApiKeyException
from wanikani_api.url_builder import UrlBuilder


class Client:
    def __init__(self, v2_api_key):
        self.v2_api_key = v2_api_key
        self.headers = {"Authorization": "Bearer {}".format(v2_api_key)}
        self.url_builder = UrlBuilder(constants.ROOT_WK_API_URL)

    def user_information(self):
        response = requests.get(
            self.url_builder.build_wk_url("user", locals()), headers=self.headers
        )
        return self._serialize_wanikani_response(response)

    def subjects(
        self,
        ids=None,
        types=None,
        slugs=None,
        levels=None,
        hidden=None,
        updated_after=None,
    ):
        response = requests.get(
            self.url_builder.build_wk_url("subjects", parameters=locals()),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def assignments(
        self,
        resource_id=None,
        ids=None,
        created_at=None,
        subject_ids=None,
        subject_types=None,
        levels=None,
        available_before=None,
        available_after=None,
        srs_stages=None,
        unlocked=None,
        started=None,
        passed=None,
        burned=None,
        resurrected=None,
        hidden=None,
        updated_after=None,
    ):
        response = requests.get(
            self.url_builder.build_wk_url(
                "assignments", resource_id=resource_id, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def review_statistics(
        self,
        resource_id=None,
        ids=None,
        subject_ids=None,
        subject_types=None,
        updated_after=None,
        percentages_greater_than=None,
        percentages_less_than=None,
        hidden=None,
    ):
        response = requests.get(
            self.url_builder.build_wk_url(
                "review_statistics", resource_id=resource_id, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def study_materials(
        self,
        resource_id=None,
        ids=None,
        subject_ids=None,
        subject_types=None,
        hidden=None,
        updated_after=None,
    ):
        response = requests.get(
            self.url_builder.build_wk_url(
                "study_materials", resource_id=resource_id, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def summary(self):
        response = requests.get(
            self.url_builder.build_wk_url("summary", parameters=locals()),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def reviews(self, resource_id=None, ids=None, subject_ids=None, updated_after=None):
        response = requests.get(
            self.url_builder.build_wk_url(
                "reviews", resource_id=resource_id, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def level_progressions(self, resource_id=None, ids=None, updated_after=None):
        response = requests.get(
            self.url_builder.build_wk_url(
                "level_progressions", resource_id=resource_id, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def resets(self, resource_id=None, ids=None, updated_after=None):
        response = requests.get(
            self.url_builder.build_wk_url("resets", parameters=locals()),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def _serialize_wanikani_response(self, response):
        if response.status_code == 200:
            json = response.json()
            return models.factory(json)
        elif response.status_code == 401:
            raise InvalidWanikaniApiKeyException(
                "[{}] is not a valid API key!".format(self.v2_api_key)
            )
