import re

from wanikani_api import constants
from .response_mocks import *


def mock_subjects(requests_mock):
    requests_mock.get(
        re.compile(constants.SUBJECT_ENDPOINT),
        json=SUBJECTS_PAGE,
        headers={"Etag": "abc123"},
    )


def mock_single_subject(requests_mock):
    requests_mock.get(
        re.compile(constants.SINGLE_SUBJECT_ENPOINT),
        json=SINGLE_SUBJECT,
        headers={"Etag": "abc123"},
    )


def mock_empty_subjects(requests_mock):
    requests_mock.get(
        re.compile(constants.SUBJECT_ENDPOINT),
        json=EMPTY_SUBJECTS_PAGE,
        headers={"Etag": "abc123"},
    )


# When making multiple calls to the subject endpoint, only answer with real data once, then just return a 304.
def mock_subjects_with_cache(requests_mock):
    requests_mock.register_uri(
        "GET",
        re.compile(constants.SUBJECT_ENDPOINT),
        [
            {"json": SUBJECTS_PAGE, "status_code": 200, "headers": {"Etag": "abc123"}},
            {"json": None, "status_code": 304},
        ],
    )


def mock_user_info(requests_mock):
    requests_mock.get(
        re.compile(constants.USER_ENDPOINT),
        json=USER_INFORMATION,
        headers={"Etag": "abc123"},
    )


def mock_assignments(requests_mock):
    requests_mock.get(
        re.compile(constants.ASSIGNMENT_ENDPOINT),
        json=ASSIGNMENTS_PAGE,
        headers={"Etag": "abc123"},
    )


def mock_review_statistics(requests_mock):
    requests_mock.get(
        re.compile(constants.REVIEW_STATS_ENDPOINT),
        json=REVIEW_STATISTICS_PAGE,
        headers={"Etag": "abc123"},
    )


def mock_level_progressions(requests_mock):
    requests_mock.get(
        re.compile(constants.LEVEL_PROGRESSIONS_ENDPOINT),
        json=LEVEL_PROGRESSIONS_PAGE,
        headers={"Etag": "abc123"},
    )


def mock_summary(requests_mock):
    requests_mock.get(
        re.compile(constants.SUMMARY_ENDPOINT), json=SUMMARY, headers={"Etag": "abc123"}
    )


def mock_resets(requests_mock):
    requests_mock.get(
        re.compile(constants.RESETS_ENDPOINT),
        json=RESETS_PAGE,
        headers={"Etag": "abc123"},
    )


def mock_reviews(requests_mock):
    requests_mock.get(
        re.compile(constants.REVIEWS_ENDPOINT),
        json=REVIEWS_PAGE,
        headers={"Etag": "abc123"},
    )


def mock_study_materials(requests_mock):
    requests_mock.get(
        re.compile(constants.STUDY_MATERIALS_ENDPOINT),
        json=STUDY_MATERIALS_PAGE,
        headers={"Etag": "abc123"},
    )
