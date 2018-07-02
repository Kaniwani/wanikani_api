#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import datetime

import requests

from wanikani_api.client import Client


def test_url_builder_with_no_parameters():
    expected = "https://api.wanikani.com/v2/user"
    actual = Client("api_key")._build_wanikani_api_url("user")
    assert actual == expected


def test_url_builder_with_single_string_parameter():
    expected = "https://api.wanikani.com/v2/subjects?types=vocabulary"
    actual = Client("api_key")._build_wanikani_api_url("subjects", {"types": "vocabulary"})
    assert actual == expected


def test_url_builder_with_single_array_parameter():
    expected = "https://api.wanikani.com/v2/subjects?types=vocabulary,kanji,radicals"
    actual = Client("api_key")._build_wanikani_api_url("subjects", {"types": ["vocabulary", "kanji", "radicals"]})
    assert actual == expected


def test_url_builder_with_multiple_string_parameter():
    expected = "https://api.wanikani.com/v2/subjects?types=vocabulary&slugs=女"
    actual = Client("api_key")._build_wanikani_api_url("subjects", {"types": "vocabulary", "slugs": "女"})
    assert actual == expected


def test_url_builder_with_single_integer_parameter():
    expected = "https://api.wanikani.com/v2/subjects?ids=1"
    actual = Client("api_key")._build_wanikani_api_url("subjects", {"ids": 1})
    assert actual == expected


def test_subject_parameters_are_properly_converted(mocker):
    mocker.patch("requests.get")
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    client.subjects(ids=[1, 2, 3], hidden=False, slugs=["abc", "123"])

    assert requests.get.call_count == 1
    requests.get.assert_called_once_with("https://api.wanikani.com/v2/subjects?hidden=false&slugs=abc,123&ids=1,2,3", headers=client.headers)

def test_parameters_convert_datetime_to_string_correctly(mocker):
    mocker.patch("requests.get")
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)
    now = datetime.datetime.now()

    client.subjects(updated_after=now)

    assert requests.get.call_count == 1
    requests.get.assert_called_once_with("https://api.wanikani.com/v2/subjects?updated_after=" + now.isoformat(), headers=client.headers)
