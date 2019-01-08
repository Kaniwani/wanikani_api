#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""

from wanikani_api.client import Client
from wanikani_api.models import Subject, UserInformation
from tests.utils.utils import (
    mock_user_info,
    mock_subjects,
    mock_assignments,
    mock_review_statistics,
    mock_study_materials,
    mock_summary,
    mock_reviews,
    mock_level_progressions,
    mock_resets,
    mock_subjects_with_cache,
    mock_single_subject,
)


def test_client_can_get_user_information(requests_mock):
    mock_user_info(requests_mock)

    client = Client("v2_api_key")

    user = client.user_information()
    assert isinstance(user, UserInformation)


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
    client = Client("v2_api_key")

    review_statistics = client.review_statistics()
    assert len(review_statistics.current_page.data) > 0


def test_client_can_get_study_materials(requests_mock):
    mock_study_materials(requests_mock)
    client = Client("v2_api_key")

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
    client = Client("v2_api_key")

    reviews = client.reviews()
    assert len(reviews.current_page.data) > 0


def test_client_can_get_level_progression(requests_mock):
    mock_level_progressions(requests_mock)
    client = Client("v2_api_key")

    progressions = client.level_progressions()
    assert len(progressions.current_page.data) > 0


def test_client_can_get_resets(requests_mock):
    mock_resets(requests_mock)
    client = Client("v2_api_key")

    resets = client.resets()
    assert len(resets.current_page.data) == 1


def test_singular_subject_retrieval(requests_mock):
    mock_single_subject(requests_mock)
    v2_api_key = "arbitrary_api_key"
    client = Client(v2_api_key)

    subject = client.subject(1)
    assert isinstance(subject, Subject)


def test_client_uses_cache(requests_mock):
    mock_subjects(requests_mock)
    mock_assignments(requests_mock)
    v2_api_key = "arbitrary_api_key"
    client = Client(v2_api_key, subject_cache_enabled=True)
    assignments = client.assignments()
    for ass in assignments:
        print(ass.subject.level)  # in theory here, if we have _not_ cached

    assert requests_mock.call_count == 2
    history = requests_mock.request_history
    assert "subjects" in history[0].url
    assert "assignments" in history[1].url


def test_etag_cache_decorator_works(mocker, requests_mock):
    mock_subjects_with_cache(requests_mock)
    v2_api_key = "arbitrary_api_key"
    client = Client(v2_api_key)

    mocker.spy(client, "_fetch_result_from_cache")
    subjects = client.subjects()
    cached_subjects = client.subjects()
    assert client._fetch_result_from_cache.call_count == 1
