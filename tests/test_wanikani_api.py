#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import datetime

from wanikani_api.client import Client
from wanikani_api.models import Subject


def test_client_can_get_user_information():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    user = client.user_information()

    assert isinstance(user.level, int)
    assert isinstance(user.profile_url, str)
    assert isinstance(user.id, type(None))
    assert isinstance(user.max_level_granted_by_subscription, int)
    assert isinstance(user.username, str)
    assert isinstance(user.subscribed, bool)
    assert isinstance(user.started_at, datetime.date)
    assert isinstance(user.current_vacation_started_at, type(None))


def test_client_can_get_subjects():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    subjects = client.subjects()
    assert len(subjects.data) > 0
    assert subjects.data[0].resource in ["vocabulary", "kanji", "radical"]


def test_client_can_get_assignments():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    assignments = client.assignments()
    assert len(assignments.data) > 0
    first_assignment = assignments.data[0]
    single_assignment = client.assignments(first_assignment.id)
    assert single_assignment.id == first_assignment.id


def test_client_can_get_review_statistics():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    review_statistics = client.review_statistics()
    assert len(review_statistics.data) > 0


def test_client_can_get_study_materials():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    study_materials = client.study_materials()
    assert len(study_materials.data) > 0


def test_client_can_get_summary():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    summary = client.summary()
    assert summary.lessons is not None
    assert summary.reviews is not None


def test_client_can_get_reviews():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    reviews = client.reviews()
    assert len(reviews.data) > 0


def test_client_can_get_level_progression():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    progressions = client.level_progressions()
    assert len(progressions.data) > 0


def test_client_can_get_resets():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    resets = client.resets()
    assert len(resets.data) == 0

def test_subject_endpoint():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    subject = client.subject(1)
    assert isinstance(subject, Subject)


