import requests

from wanikani_api import constants, models
from wanikani_api.exceptions import InvalidWanikaniApiKeyException
from wanikani_api.models import Iterator
from wanikani_api.subjectcache import SubjectCache
from wanikani_api.url_builder import UrlBuilder
from copy import deepcopy


"""
This is the primary point of entry for accessing the Wanikani API.
"""


class Client:
    """
    This is the only object you can instantiate. It provides access to each
    relevant API endpoint on Wanikani.
    """

    def __init__(self, v2_api_key, subject_cache_enabled=False):
        self.v2_api_key = v2_api_key
        self.headers = {"Authorization": "Bearer {}".format(v2_api_key)}
        self.url_builder = UrlBuilder(constants.ROOT_WK_API_URL)
        self.subject_cache = None
        self.etag_cache = {}
        self.authorized_request_maker = self.build_authorized_requester(self.headers)
        if subject_cache_enabled:
            self.use_local_subject_cache()

    def _fetch_result_from_cache(self, request_key):
        return self.etag_cache[request_key]["result"]

    def _fetch_etag_from_cache(self, request_key):
        return self.etag_cache[request_key]["etag"]

    def _store_in_cache(self, request_key, response):
        etag = response.headers["Etag"]
        self.etag_cache[request_key]["etag"] = etag
        self.etag_cache[request_key]["result"] = self._serialize_wanikani_response(
            response
        )

    def build_authorized_requester(self, headers):
        def _make_wanikani_api_request(url):
            request_key = (url, headers["Authorization"])
            request_headers = deepcopy(headers)
            try:
                etag = self.etag_cache[request_key]["etag"]
                request_headers["If-None-Match"] = etag
            except KeyError:
                self.etag_cache[request_key] = {}
            finally:
                response = requests.get(url, headers=request_headers)
                if response.status_code == 304:
                    return self._fetch_result_from_cache(request_key)
                elif response.status_code == 200:
                    self._store_in_cache(request_key, response)
                    return self.etag_cache[request_key]["result"]
                else:
                    raise Exception(f"Failed to contact Wanikani: {response.content}")

        return _make_wanikani_api_request

    def use_local_subject_cache(self):
        self.subject_cache = SubjectCache(self.subjects(fetch_all=True))

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
        if self.subject_cache:
            return self.subject_cache.get(subject_id)
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
        fetch_all=False,
    ):
        """Retrieves Subjects

        Wanikani refers to Radicals, Kanji, and Vocabulary as Subjects. This function allows you to fetch all of
        the subjects, regardless of the current level of the account that the API key is associated to. All parameters
        to this function are optional, and are for filtering the results.
        are ignored, and the subject with that ID in question is fetched.

        :param int[] ids: Filters based on a list of IDs. Does not cause other parameters to be ignored.
        :param str[] types: The specific :class:`.models.Subject` types you wish to retrieve. Possible values are: ``["kanji", "vocabulary", "radicals"]``
        :param str[] slugs: The wanikani slug
        :param int[] levels: Include only :class:`.models.Subject` from the specified levels.
        :param bool hidden: Return :class:`.models.Subject` which are or are not hidden from the user-facing application
        :param bool fetch_all: if set to True, instead of fetching only first page of results, will fetch them all.
        :param  updated_after: Return results which have been updated after the timestamp
        :type updated_after: :class:`datetime.datetime`
        :return: An iterator over multiple :class:`models.Page` , in which the ``data`` field contains a list anything that is a :class:`.models.Subject`, e.g.:

            * :class:`.models.Radical`
            * :class:`.models.Kanji`
            * :class:`.models.Vocabulary`
        """

        url = self.url_builder.build_wk_url(
            constants.SUBJECT_ENDPOINT, parameters=locals()
        )
        return self._wrap_collection_in_iterator(
            self.authorized_request_maker(url), fetch_all
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
        fetch_all=False,
    ):
        """
        Assignments are the association between a user, and a subject. This means that every time something is added to
        your lessons, a new :class:`.models.Assignment` is created.

        :param bool fetch_all: if set to True, instead of fetching only first page of results, will fetch them all.
        :param int[] ids: Return only results with the given IDs
        :param created_at: Timestamp when resource was created
        :param int[] subject_ids: Return only :class:`.models.Assignment`s which are tied to the given subject_ids
        :param str[] subject_types: The specific :class:`.models.Subject` types you wish to retrieve. Possible values are: ``["kanji", "vocabulary", "radicals"]``
        :param int[] levels: Include only :class:`.models.Assignment` where the subjects are from the specified levels.
        :param datetime available_before: Return assignment reviews available before timestamp
        :param datetime available_after: Return assignment reviews available after timestamp
        :param int srs_stages: Return assignments of specified srs stages. Note, 0 is lessons, 9 is the burned state
        :param bool unlocked: Return assignments which have unlocked (made available to lessons)
        :param bool started: Return assignments which move from lessons to reviews
        :param bool passed: Return assignments which have reach Guru (aka srs_stage 5) at some point (true) or which have never been Guru’d (false)
        :param bool burned: Return assignments which have been burned at some point (true) or never have been burned (false)
        :param bool resurrected: Return assignments which either have been resurrect (true) or not (false)
        :param bool hidden: Return assignments which are or are not hidden from the user-facing application
        :param datetime updated_after: Return results which have been updated after the timestamp
        :return: An iterator over a set of :class:`.models.Page` where the data contained is all :class:`.models.Assignment`
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.ASSIGNMENT_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response), fetch_all
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
        fetch_all=False,
    ):
        """
        Retrieve all Review Statistics from Wanikani. A Review Statistic is related to a single subject which the user has studied.

        :param bool fetch_all: if set to True, instead of fetching only first page of results, will fetch them all.
        :param int[] ids: Return only results with the given IDs
        :param int[] subject_ids: Return only :class:`.models.Assignment`s which are tied to the given subject_ids
        :param str[] subject_types: The specific :class:`.models.Subject` types you wish to retrieve. Possible values are: ``["kanji", "vocabulary", "radicals"]``
        :param datetime updated_after: Return results which have been updated after the timestamp
        :param int percentages_greater_than: Return results where the percentage_correct is greater than the value. [0-100]
        :param int percentages_less_than: Return results where the percentage_correct is less than the value. [0-100]
        :param bool hidden: Return only results where the related subject has been hidden.
        :return: An iterator which contains all Review Statistics
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.REVIEW_STATS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response), fetch_all
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
        fetch_all=False,
    ):
        """
        Retrieve all Study Materials. These are primarily meaning notes, reading notes, and meaning synonyms.

        :param bool fetch_all: if set to True, instead of fetching only first page of results, will fetch them all.
        :param int[] ids: Return only results with the given IDs
        :param int[] subject_ids: Return only :class:`.models.Assignment`s which are tied to the given subject_ids
        :param str[] subject_types: The specific :class:`.models.Subject` types you wish to retrieve. Possible values are: ``["kanji", "vocabulary", "radicals"]``
        :param bool hidden: Return only results where the related subject has been hidden.
        :param datetime updated_after: Return results which have been updated after the timestamp
        :return: An iterator over all Study Materials
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.STUDY_MATERIALS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response), fetch_all
        )

    def summary(self):
        """

        :return:
        """
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

    def reviews(self, ids=None, subject_ids=None, updated_after=None, fetch_all=False):
        """
        Retrieve all reviews for a given user. A :class:`.models.Review` is a single instance of this user getting a
        single review correctly submitted.

        :param bool fetch_all: if set to True, instead of fetching only first page of results, will fetch them all.
        :param int[] ids: Return only results with the given IDs
        :param int[] subject_ids: Return only :class:`.models.Assignment`s which are tied to the given subject_ids
        :param datetime updated_after: Return results which have been updated after the timestamp
        :return: An iterator over all :class:`.models.Review` for a given user.
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.REVIEWS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response), fetch_all
        )

    def level_progression(self, level_progression_id):
        """
        Get a single :class:`.models.LevelProgression` by its known id

        :param level_progression_id: the id of the level_progression
        :return: a single :class:`.models.LevelProgression`
        """
        url = self.url_builder.build_wk_url(
            constants.LEVEL_PROGRESSIONS_ENDPOINT, resource_id=level_progression_id
        )
        return self.authorized_request_maker(url)

    def level_progressions(self, ids=None, updated_after=None, fetch_all=False):
        """
        Retrieve all :class:`.models.LevelProgression` for a given user.

        :param bool fetch_all: if set to True, instead of fetching only first page of results, will fetch them all.
        :param int[] ids: Return only results with the given IDs
        :param datetime updated_after: Return results which have been updated after the timestamp
        :return: An iterator over all :class:`.models.LevelProgression` for a given user.
        """
        url = (
            self.url_builder.build_wk_url(
                constants.LEVEL_PROGRESSIONS_ENDPOINT, parameters=locals()
            ),
        )
        return self._wrap_collection_in_iterator(
            self.authorized_request_maker(url), fetch_all
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

    def resets(self, ids=None, updated_after=None, fetch_all=False):
        """
        Retrieve information for all resets the user has performed on Wanikani.

        :param bool fetch_all: if set to True, instead of fetching only first page of results, will fetch them all.
        :param int[] ids: Return only results with the given IDs
        :param datetime updated_after: Return results which have been updated after the timestamp
        :return: An iterator over all :class:`.models.Reset` for a given user.
        """
        response = requests.get(
            self.url_builder.build_wk_url(
                constants.RESETS_ENDPOINT, parameters=locals()
            ),
            headers=self.headers,
        )
        return self._wrap_collection_in_iterator(
            self._serialize_wanikani_response(response), fetch_all
        )

    def _serialize_wanikani_response(self, response):
        if response.status_code == 200:
            json = response.json()
            return models.factory(json, client=self)
        elif response.status_code == 401:
            raise InvalidWanikaniApiKeyException(
                "[{}] is not a valid API key!".format(self.v2_api_key)
            )

    def _wrap_collection_in_iterator(self, resource, fetch_all):
        return Iterator(
            current_page=resource,
            api_request=self.authorized_request_maker,
            fetch_all=fetch_all,
        )
