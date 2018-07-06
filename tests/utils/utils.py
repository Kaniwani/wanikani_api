import re

from wanikani_api import constants
from .response_mocks import *


def mock_subjects(requests_mock):
    requests_mock.get(constants.ROOT_WK_API_URL + constants.SUBJECT_ENDPOINT, json=SUBJECTS_PAGE)


def mock_user_info(requests_mock):
    requests_mock.get(re.compile(constants.USER_ENDPOINT), json=USER_INFORMATION)


def mock_assignments(requests_mock):
    requests_mock.get(re.compile(constants.ASSIGNMENT_ENDPOINT), json=ASSIGNMENTS_PAGE)


def mock_review_statistics(requests_mock):
    requests_mock.get(re.compile(constants.REVIEW_STATS_ENDPOINT), json=REVIEW_STATISTICS_PAGE)


def mock_level_progressions(requests_mock):
    requests_mock.get(re.compile(constants.LEVEL_PROGRESSIONS_ENDPOINT), json=LEVEL_PROGRESSIONS_PAGE)

def mock_summary(requests_mock):
    requests_mock.get(re.compile(constants.SUMMARY_ENDPOINT), json=SUMMARY)

def mock_resets(requests_mock):
    requests_mock.get(re.compile(constants.RESETS_ENDPOINT), json=RESETS_PAGE)

def mock_reviews(requests_mock):
    requests_mock.get(re.compile(constants.REVIEWS_ENDPOINT), json=REVIEWS_PAGE)

def mock_study_materials(requests_mock):
    requests_mock.get(re.compile(constants.STUDY_MATERIALS_ENDPOINT), json=STUDY_MATERIALS_PAGE)
