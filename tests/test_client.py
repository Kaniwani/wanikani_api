#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import datetime

import requests
from tests.utils.utils import mock_subjects

from wanikani_api.client import Client
from wanikani_api.models import Iterator


def test_subject_parameters_are_properly_converted(mocker):
    mocker.patch("requests.get")
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    client.subjects(ids=[1, 2, 3], hidden=False, slugs=["abc", "123"])

    assert requests.get.call_count == 1
    requests.get.assert_called_once_with("https://api.wanikani.com/v2/subjects?hidden=false&ids=1,2,3&slugs=abc,123", headers=client.headers)


def test_client_correctly_renders_empty_collections():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)
    response = client.subjects(ids=[1, 2, 3], hidden=False, slugs=["abc", "123"])
    assert len(response.current_page.data) == 0


def test_parameters_convert_datetime_to_string_correctly(mocker):
    mocker.patch("requests.get")
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)
    now = datetime.datetime.now()

    client.subjects(updated_after=now)

    assert requests.get.call_count == 1
    requests.get.assert_called_once_with("https://api.wanikani.com/v2/subjects?updated_after=" + now.isoformat(), headers=client.headers)


def test_requests_mock(requests_mock):
    mock_subjects(requests_mock)

    client = Client('whatever')
    subjects = client.subjects()
    assert isinstance(subjects, Iterator)


