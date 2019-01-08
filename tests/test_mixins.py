#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import requests

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
    mock_single_subject,
)


def test_subjectable_mixin_works(requests_mock):
    mock_subjects(requests_mock)
    mock_assignments(requests_mock)
    client = Client("arbitrary_api_key", subject_cache_enabled=True)

    assignments = client.assignments()
    assignment = assignments[0]
    subj = assignment.subject
    assert subj.id == assignment.subject_id


def test_expected_subjectable_resources_work(requests_mock):
    mock_assignments(requests_mock)
    mock_summary(requests_mock)
    mock_subjects(requests_mock)
    mock_reviews(requests_mock)
    mock_single_subject(requests_mock)
    mock_study_materials(requests_mock)
    mock_summary(requests_mock)

    client = Client("arbitrary_api_key")

    assignments = client.assignments()
    assert assignments[0].subject is not None

    study_materials = client.study_materials()
    assert study_materials[0].subject is not None

    study_materials = client.study_materials()
    assert study_materials[0].subject is not None

    summary = client.summary()
    assert summary.reviews[0].subjects is not None

    reviews = client.reviews()
    assert reviews[0].subject is not None
