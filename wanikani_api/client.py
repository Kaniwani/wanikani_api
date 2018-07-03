import requests

from wanikani_api import constants, models
from wanikani_api.exceptions import InvalidWanikaniApiKeyException
from wanikani_api.url_builder import UrlBuilder


"""
This is the primary point of entry for accessing the Wanikani API.
"""


class Client:
    """
    This is the only object you can instantiate. It provides access to each
    relevant API endpoint on Wanikani.
    """

    def __init__(self, v2_api_key):
        self.v2_api_key = v2_api_key
        self.headers = {"Authorization": "Bearer {}".format(v2_api_key)}
        self.url_builder = UrlBuilder(constants.ROOT_WK_API_URL)

    def user_information(self):
        """
        Gets all relevant information about the user.

        :raises: :class:`.exceptions.InvalidWanikaniApiKeyException`
        :rtype: :class:`.models.UserInformation`
        """
        response = requests.get(
            self.url_builder.build_wk_url("user", locals()), headers=self.headers
        )
        return self._serialize_wanikani_response(response)

    def subjects(
        self,
        resource_id=None,
        ids=None,
        types=None,
        slugs=None,
        levels=None,
        hidden=None,
        updated_after=None,
    ):
        """Retrieves Subjects

        Wanikani refers to Radicals, Kanji, and Vocabulary as Subjects. This function allows you to fetch all of
        the subjects, regardless of the current level of the account that the API key is associated to. All parameters
        to this function are optional, and are for filtering the results.
        are ignored, and the subject with that ID in question is fetched.

        :param int resource_id: The ID of the remote resource. If this is passed, all other parameters are ignored, and we just fetch this one resource.
        :param int[] ids: Similar to ``resource_id`` but instead filters based on a list of IDs. Does not cause other parameters to be ignored.
        :param str[] types: The specific :class:`.models.Subject` types you wish to retrieve. Possible values are: ``["kanji", "vocabulary", "radicals"]``
        :param str[] slugs: TODO figure out what this is.
        :param int[] levels: Include only :class:`.models.Subject` from the specified levels.
        :param bool hidden: Return :class:`.models.Subject` which are or are not hidden from the user-facing application
        :param  updated_after: Return results which have been updated after the timestamp
        :type updated_after: :class:`datetime.datetime`
        :return: A :class:`models.Collection` , in which the ``data`` field contains a list anything that is a :class:`.models.Subject`, e.g.:

            * :class:`.models.Radical`
            * :class:`.models.Kanji`
            * :class:`.models.Vocabulary`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                "subjects", resource_id=resource_id, parameters=locals()
            ),
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
