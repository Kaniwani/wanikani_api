#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import datetime

import pytest
import requests

from tests.utils.utils import mock_subjects, mock_assignments
from wanikani_api.client import Client
from wanikani_api.constants import ROOT_WK_API_URL


@pytest.fixture
def url_builder():
    from wanikani_api.url_builder import UrlBuilder

    return UrlBuilder(ROOT_WK_API_URL)


def test_url_builder_with_no_parameters(url_builder):
    expected = "https://api.wanikani.com/v2/user"
    actual = url_builder.build_wk_url("user")
    assert actual == expected


def test_url_builder_with_single_string_parameter(url_builder):
    expected = "https://api.wanikani.com/v2/subjects?types=vocabulary"
    actual = url_builder.build_wk_url("subjects", {"types": "vocabulary"})
    assert actual == expected


def test_url_builder_with_single_array_parameter(url_builder):
    expected = "https://api.wanikani.com/v2/subjects?types=vocabulary,kanji,radicals"
    actual = url_builder.build_wk_url(
        "subjects", {"types": ["vocabulary", "kanji", "radicals"]}
    )
    assert actual == expected


def test_url_builder_with_multiple_string_parameter(url_builder):
    expected = "https://api.wanikani.com/v2/subjects?slugs=女&types=vocabulary"
    actual = url_builder.build_wk_url("subjects", {"types": "vocabulary", "slugs": "女"})
    assert actual == expected


def test_url_builder_with_single_integer_parameter(url_builder):
    expected = "https://api.wanikani.com/v2/subjects?ids=1"
    actual = url_builder.build_wk_url("subjects", {"ids": 1})
    assert actual == expected


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


def test_assignment_parameters_are_properly_converted(requests_mock):
    mock_assignments(requests_mock)
    v2_api_key = "arbitrary_api_key"
    client = Client(v2_api_key)

    client.assignments(ids=[1, 2, 3], hidden=False, srs_stages=[0, 1, 2])

    assert requests_mock.call_count == 1
    assert (
        requests_mock.request_history[0].url
        == "https://api.wanikani.com/v2/assignments?hidden=false&ids=1,2,3&srs_stages=0,1,2"
    )
