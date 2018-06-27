#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import datetime

import pytest

from wanikani_api.client import Client
from wanikani_api.models import User


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_client_can_get_user_information():
    v2_api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"
    client = Client(v2_api_key)

    api_response = client.user_information()
    assert api_response.status_code == 200

    user = User(api_response.json())

    assert isinstance(user.level, int)
    assert isinstance(user.profile_url, str)
    assert isinstance(user.id, type(None))
    assert isinstance(user.max_level_granted_by_subscription, int)
    assert isinstance(user.username, str)
    assert isinstance(user.subscribed, bool)
    assert isinstance(user.started_at, datetime.date)
    assert isinstance(user.current_vacation_started_at, datetime.date or None)


def test_client_can_get_subjects():
    pass


def test_client_can_get_assignments():
    pass


def test_client_can_get_review_statistics():
    pass


def test_client_can_get_study_materials():
    pass


def test_client_can_get_summary():
    pass


def test_client_can_get_reviews():
    pass


def test_client_can_get_level_progression():
    pass


def test_client_can_get_resets():
    pass
