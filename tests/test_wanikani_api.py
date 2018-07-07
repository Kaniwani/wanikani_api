#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import datetime

from wanikani_api.client import Client
from wanikani_api.models import Subject
from tests.utils.utils import mock_user_info, mock_subjects, mock_assignments, mock_review_statistics, \
    mock_study_materials, mock_summary, mock_reviews, mock_level_progressions, mock_resets


def test_client_can_get_user_information(requests_mock):
    mock_user_info(requests_mock)

    client = Client("v2_api_key")

    user = client.user_information()

    assert isinstance(user.level, int)
    assert isinstance(user.profile_url, str)
    assert isinstance(user.id, type(None))
    assert isinstance(user.max_level_granted_by_subscription, int) #TODO START HEER REPLACINBG v2_api_key with string
    assert isinstance(user.username, str)
    assert isinstance(user.subscribed, bool)
    assert isinstance(user.started_at, datetime.date)
    assert isinstance(user.current_vacation_started_at, type(None))


def test_client_can_get_subjects(requests_mock):
    mock_subjects(requests_mock)

    client = Client("v2_api_key")

    subjects = client.subjects()
    assert len(subjects.current_page.data) > 0
    assert subjects.current_page.data[0].resource in ["vocabulary", "kanji", "radical"]


def test_client_can_get_assignments(requests_mock):
    mock_assignments(requests_mock)

    client = Client("v2_api_key")

    assignments = client.assignments()

    assert len(assignments.current_page.data) > 0

def test_client_can_get_review_statistics(requests_mock):
    mock_review_statistics(requests_mock)
    "v2_api_key" = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client("v2_api_key")

    review_statistics = client.review_statistics()
    assert len(review_statistics.current_page.data) > 0


def test_client_can_get_study_materials(requests_mock):
    mock_study_materials(requests_mock)
    client = Client(v2_api_key)

    study_materials = client.study_materials()
    assert len(study_materials.current_page.data) > 0


def test_client_can_get_summary(requests_mock):
    mock_summary(requests_mock)
    client = Client("v2_api_key")

    summary = client.summary()
    assert summary.lessons is not None
    assert summary.reviews is not None


def test_client_can_get_reviews(requests_mock):
    mock_reviews(requests_mock)
    client = Client(v2_api_key)

    reviews = client.reviews()
    assert len(reviews.current_page.data) > 0


def test_client_can_get_level_progression(requests_mock):
    mock_level_progressions(requests_mock)
    client = Client(v2_api_key)

    progressions = client.level_progressions()
    assert len(progressions.current_page.data) > 0


def test_client_can_get_resets(requests_mock):
    mock_resets(requests_mock)
    client = Client("v2_api_key")

    resets = client.resets()
    assert len(resets.current_page.data) == 0

def test_singular_endpoint():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    subject = client.subject(1)
    assert isinstance(subject, Subject)


def test_limits_are_respected(requests_mock):
    mock_subjects(requests_mock)
    client = Client(v2_api_key)

    subjects = client.subjects(max_results=1)
    assert len(list(subjects)) == 1
