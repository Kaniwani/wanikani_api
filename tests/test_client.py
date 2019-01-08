#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import datetime

import requests
from tests.utils.utils import mock_subjects, mock_empty_subjects

from wanikani_api.client import Client
from wanikani_api.models import Iterator


class Empty200:
    def __init__(self):
        self.status_code = 200


class MockedRequest:
    def __init__(self, *args, **kwargs):
        self.status_code = 200


def test_subject_parameters_are_properly_converted(requests_mock):
    mock_subjects(requests_mock)

    v2_api_key = "arbitrary_api_key"
    client = Client(v2_api_key)

    client.subjects(ids=[1, 2, 3], hidden=False, slugs=["abc", "123"])

    assert requests_mock.call_count == 1
    assert (
        requests_mock.request_history[0].url
        == "https://api.wanikani.com/v2/subjects?hidden=false&ids=1,2,3&slugs=abc,123"
    )


def test_client_correctly_renders_empty_collections(requests_mock):
    mock_empty_subjects(requests_mock)
    v2_api_key = "arbitrary_api_key"
    client = Client(v2_api_key)
    response = client.subjects(ids=[1, 2, 3], hidden=False, slugs=["abc", "123"])
    assert len(response.current_page.data) == 0


def test_parameters_convert_datetime_to_string_correctly(requests_mock):
    mock_subjects(requests_mock)
    v2_api_key = "arbitrary_api_key"
    client = Client(v2_api_key)
    now = datetime.datetime.now()

    client.subjects(updated_after=now)

    assert requests_mock.call_count == 1
    assert (
        requests_mock.request_history[0].url
        == "https://api.wanikani.com/v2/subjects?updated_after=" + now.isoformat()
    )


def test_requests_mock(requests_mock):
    mock_subjects(requests_mock)

    client = Client("whatever")
    subjects = client.subjects()
    assert isinstance(subjects, Iterator)
