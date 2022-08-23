#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""

from wanikani_api.client import Client
from wanikani_api.models import Subject, UserInformation, Kanji, Radical, Vocabulary
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

api_key = "2510f001-fe9e-414c-ba19-ccf79af40060"


def test_real_connection_to_wanikani_user_information():
    client = Client(api_key)

    user = client.user_information()
    assert isinstance(user, UserInformation)

def test_real_connection_to_subjects():
    client = Client(api_key)
    subjects = client.subjects()
    assert len(subjects.current_page.data) > 0
    assert subjects.current_page.data[0].resource in ["vocabulary", "kanji", "radical"]

def test_vocabulary_connection_gets_all_known_data():
    client = Client(api_key)
    subject = client.subject(subject_id=2467)
    assert isinstance(subject, Vocabulary)
    assert subject.level == 1
    assert subject.slug == "一"
    assert subject.hidden_at == None
    assert subject.document_url == "https://www.wanikani.com/vocabulary/%E4%B8%80"
    assert subject.url == "https://api.wanikani.com/v2/subjects/2467"
    assert len(subject.meanings) == 1
    assert len(subject.auxiliary_meanings) == 1
    assert len(subject.readings) == 1
    assert len(subject.parts_of_speech) == 1
    assert len(subject.component_subject_ids) == 1
    assert subject.meaning_mnemonic == "As is the case with most vocab words that consist of a single kanji, this vocab word has the same meaning as the kanji it parallels, which is <vocabulary>one</vocabulary>."
    assert subject.reading_mnemonic == "When a vocab word is all alone and has no okurigana (hiragana attached to kanji) connected to it, it usually uses the kun'yomi reading. Numbers are an exception, however. When a number is all alone, with no kanji or okurigana, it is going to be the on'yomi reading, which you learned with the kanji.  Just remember this exception for alone numbers and you'll be able to read future number-related vocab to come."
    assert len(subject.context_sentences) == 3
    first_sentence = subject.context_sentences[0]
    assert first_sentence.english == "Let’s meet up once."
    assert first_sentence.japanese == "一ど、あいましょう。"
    assert len(subject.pronunciation_audios) == 8
    assert subject.lesson_position == 44
    assert subject.spaced_repitition_system_id == 2

def test_kanji_connection_gets_all_known_data():
    client = Client(api_key)
    subject = client.subject(subject_id=440)
    assert isinstance(subject, Kanji)
    assert subject.level == 1
    assert subject.slug == "一"
    assert subject.hidden_at == None
    assert subject.document_url == "https://www.wanikani.com/kanji/%E4%B8%80"
    assert subject.url == "https://api.wanikani.com/v2/subjects/440"
    assert len(subject.meanings) == 1
    assert len(subject.auxiliary_meanings) == 1
    assert len(subject.readings) == 4
    assert len(subject.component_subject_ids) == 1
    assert len(subject.amalgamation_subject_ids) == 72
    assert "Lying on the " in subject.meaning_mnemonic
    assert "To remember the meaning of" in subject.meaning_hint
    assert "As you're sitting" in subject.reading_mnemonic
    assert "Make sure you feel the" in subject.reading_hint
    assert subject.lesson_position == 26
    assert subject.spaced_repitition_system_id == 2


def test_radical_connection_gets_all_known_data():
    client = Client(api_key)
    subject = client.subject(subject_id=1)
    assert isinstance(subject, Radical)
    assert subject.level == 1
    assert subject.slug == "ground"
    assert subject.hidden_at == None
    assert subject.document_url == "https://www.wanikani.com/radicals/ground"
    assert subject.url == "https://api.wanikani.com/v2/subjects/1"
    assert len(subject.meanings) == 1
    assert len(subject.auxiliary_meanings) == 0
    assert len(subject.amalgamation_subject_ids) == 72
    assert "This radical consists of" in subject.meaning_mnemonic
    assert subject.lesson_position == 0
    assert subject.spaced_repitition_system_id == 2



def test_real_connection_to_assignments():
    client = Client(api_key)
    assignments = client.assignments()
    assert len(assignments.current_page.data) > 0

def test_real_connection_to_review_statistics():
    client = Client(api_key)
    review_statistics = client.review_statistics()
    assert len(review_statistics.current_page.data) > 0

def test_real_connection_to_study_materials():
    client = Client(api_key)
    study_materials = client.study_materials()
    assert len(study_materials.current_page.data) > 0

def test_real_connection_to_summary():
    client = Client(api_key)
    summary = client.summary()
    assert summary.lessons is not None
    assert summary.reviews is not None

def test_real_connection_to_reviews():
    client = Client(api_key)
    reviews = client.reviews()
    assert len(reviews.current_page.data) > 0

def test_real_connection_to_level_progression():
    client = Client(api_key)
    progressions = client.level_progressions()

def test_real_connection_to_resets():
    client = Client(api_key)
    resets = client.resets()
    assert len(resets.current_page.data) == 0

def test_real_connection_to_singular_subject():
    client = Client(api_key)
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
