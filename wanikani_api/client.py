import requests

from wanikani_api import constants, models
from wanikani_api.exceptions import InvalidWanikaniApiKeyException
from wanikani_api.models import Iterator, Page
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
            self.url_builder.build_wk_url(constants.USER_ENDPOINT), headers=self.headers
        )
        return self._serialize_wanikani_response(response)

    def subject(self, subject_id):
        """
        Get a single subject by its known id

        :param subject_id: the id of the subject
        :return: a single :class:`.models.Subject`. This might be either:
            * :class:`.models.Radical`
            * :class:`.models.Kanji`
            * :class:`.models.Vocabulary`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.SUBJECT_ENDPOINT, resource_id=subject_id
            ),
            headers=self.headers,
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
        max_results=None,
    ):
        """Retrieves Subjects

        Wanikani refers to Radicals, Kanji, and Vocabulary as Subjects. This function allows you to fetch all of
        the subjects, regardless of the current level of the account that the API key is associated to. All parameters
        to this function are optional, and are for filtering the results.
        are ignored, and the subject with that ID in question is fetched.

        :param int[] ids: Filters based on a list of IDs. Does not cause other parameters to be ignored.
        :param str[] types: The specific :class:`.models.Subject` types you wish to retrieve. Possible values are: ``["kanji", "vocabulary", "radicals"]``
        :param str[] slugs: TODO figure out what this is.
        :param int[] levels: Include only :class:`.models.Subject` from the specified levels.
        :param bool hidden: Return :class:`.models.Subject` which are or are not hidden from the user-facing application
        :param  updated_after: Return results which have been updated after the timestamp
        :param max_results: The maximum number of results you wish to have returned.
        :type updated_after: :class:`datetime.datetime`
        :return: An iterator over multiple :class:`models.Page` , in which the ``data`` field contains a list anything that is a :class:`.models.Subject`, e.g.:

            * :class:`.models.Radical`
            * :class:`.models.Kanji`
            * :class:`.models.Vocabulary`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.SUBJECT_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response), max_results
        )

    def assignment(self, assignment_id):
        """
        Get a single :class:`.models.Assignment` by its known id

        :param assignment_id: the id of the assignment
        :return: a single :class:`.models.Assignment`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.ASSIGNMENT_ENDPOINT, resource_id=assignment_id
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def assignments(
        self,
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
                constants.ASSIGNMENT_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response)
        )

    def review_statistic(self, review_statistic_id):
        """
        Get a single :class:`.models.ReviewStatistic` by its known id

        :param review_statistic_id: the id of the review_statistic
        :return: a single :class:`.models.ReviewStatistic`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.REVIEW_STATS_ENDPOINT, resource_id=review_statistic_id
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def review_statistics(
        self,
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
                constants.REVIEW_STATS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response)
        )

    def study_material(self, study_material_id):
        """
        Get a single :class:`.models.StudyMaterial` by its known id

        :param study_material_id: the id of the study material
        :return: a single :class:`.models.StudyMaterial`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.STUDY_MATERIALS_ENDPOINT, resource_id=study_material_id
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def study_materials(
        self,
        ids=None,
        subject_ids=None,
        subject_types=None,
        hidden=None,
        updated_after=None,
    ):
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.STUDY_MATERIALS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response)
        )

    def summary(self):
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.SUMMARY_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def review(self, review_id):
        """
        Get a single :class:`.models.Review` by its known id

        :param review_id: the id of the review
        :return: a single :class:`.models.Review`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.REVIEWS_ENDPOINT, resource_id=review_id
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def reviews(self, ids=None, subject_ids=None, updated_after=None):
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.REVIEWS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response)
        )

    def level_progression(self, level_progression_id):
        """
        Get a single :class:`.models.LevelProgression` by its known id

        :param level_progression_id: the id of the level_progression
        :return: a single :class:`.models.LevelProgression`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.LEVEL_PROGRESSIONS_ENDPOINT, resource_id=level_progression_id
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def level_progressions(self, ids=None, updated_after=None):
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.LEVEL_PROGRESSIONS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response)
        )

    def reset(self, reset_id):
        """
        Get a single :class:`.models.Reset` by its known id

        :param reset_id: the id of the reset
        :return: a single :class:`.models.Reset`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.REVIEWS_ENDPOINT, resource_id=reset_id
            ),
            headers=self.headers,
        )
        return self._serialize_wanikani_response(response)

    def resets(self, ids=None, updated_after=None):
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.RESETS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response)
        )

    def _serialize_wanikani_response(self, response):
        if response.status_code == 200:
            json = response.json()
            return models.factory(json)
        elif response.status_code == 401:
            raise InvalidWanikaniApiKeyException(
                "[{}] is not a valid API key!".format(self.v2_api_key)
            )

    def api_request(self, url):
        response = requests.get(url, headers=self.headers)
        return self._serialize_wanikani_response(response)

    def _wrap_collection_in_iterator(self, resource, max_results=None):
        return Iterator(
            current_page=resource, api_request=self.api_request, max_results=max_results
        )
