#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wanikani_api` package."""
import datetime

from tests.utils.utils import (
    mock_subjects,
    mock_empty_subjects,
    mock_assignments,
    mock_study_materials,
    mock_reviews,
)

from wanikani_api.client import Client
from wanikani_api.models import (
    Iterator,
    Vocabulary,
    Kanji,
    Radical,
    Meaning,
    ContextSentence,
    PronunciationAudio,
    AuxiliaryMeaning,
    KanjiReading,
    CharacterImage,
)


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


def test_all_vocabulary_parameters_are_imported(requests_mock):
    mock_subjects(requests_mock)

    client = Client("whatever")
    subjects = client.subjects()
    vocabulary = [subject for subject in subjects if isinstance(subject, Vocabulary)][0]
    assert vocabulary.created_at is not None
    assert vocabulary.level is not None
    assert vocabulary.slug is not None
    assert vocabulary.hidden_at is None
    assert vocabulary.document_url is not None
    assert vocabulary.characters is not None
    assert isinstance(vocabulary.meanings[0], Meaning)
    assert isinstance(vocabulary.auxiliary_meanings[0], AuxiliaryMeaning)
    assert vocabulary.parts_of_speech is not None
    assert vocabulary.component_subject_ids is not None
    assert vocabulary.meaning_mnemonic is not None
    assert vocabulary.reading_mnemonic is not None
    assert isinstance(vocabulary.context_sentences[0], ContextSentence)
    assert isinstance(vocabulary.pronunciation_audios[0], PronunciationAudio)
    assert vocabulary.lesson_position is not None


def test_all_kanji_parameters_are_imported(requests_mock):
    mock_subjects(requests_mock)

    client = Client("whatever")
    subjects = client.subjects()
    kanji = [subject for subject in subjects if isinstance(subject, Kanji)][0]
    assert kanji.created_at is not None
    assert kanji.level is not None
    assert kanji.slug is not None
    assert kanji.hidden_at is None
    assert kanji.document_url is not None
    assert kanji.characters is not None
    assert kanji.meanings is not None
    assert isinstance(kanji.auxiliary_meanings[0], AuxiliaryMeaning)
    assert isinstance(kanji.readings[0], KanjiReading)
    assert kanji.component_subject_ids is not None
    assert kanji.amalgamation_subject_ids is not None
    assert kanji.visually_similar_subject_ids is not None
    assert kanji.meaning_mnemonic is not None
    assert kanji.meaning_hint is not None
    assert kanji.reading_mnemonic is not None
    assert kanji.reading_hint is not None
    assert kanji.lesson_position is not None


def test_all_radical_parameters_are_imported(requests_mock):
    mock_subjects(requests_mock)

    client = Client("whatever")
    subjects = client.subjects()
    radical = [subject for subject in subjects if isinstance(subject, Radical)][0]
    assert radical.created_at is not None
    assert radical.level is not None
    assert radical.slug is not None
    assert radical.hidden_at is None
    assert radical.document_url is not None
    assert radical.characters is not None
    assert isinstance(radical.character_images[0], CharacterImage)
    assert radical.auxiliary_meanings is not None
    assert radical.meaning_mnemonic is not None
    assert radical.lesson_position is not None


def test_all_assignment_parameters_are_imported(requests_mock):
    mock_assignments(requests_mock)

    client = Client("whatever")
    assignments = client.assignments()
    assignment = assignments[0]

    assert assignment.created_at is not None
    assert assignment.subject_id is not None
    assert assignment.subject_type is not None
    assert assignment.srs_stage is not None
    assert assignment.srs_stage_name is not None
    assert assignment.unlocked_at is not None
    assert assignment.started_at is not None
    assert assignment.passed_at is not None
    assert assignment.burned_at is None
    assert assignment.available_at is not None
    assert assignment.resurrected_at is None
    assert assignment.passed is not None
    assert assignment.resurrected is not None
    assert assignment.hidden is not None


def test_all_study_material_parameters_are_imported(requests_mock):
    mock_study_materials(requests_mock)

    client = Client("whatever")
    study_materials = client.study_materials()
    study_material = study_materials[0]

    assert study_material.created_at is not None
    assert study_material.url is not None
    assert study_material.data_updated_at is not None
    assert study_material.subject_id is not None
    assert study_material.subject_type is not None
    assert study_material.meaning_note is not None
    assert study_material.reading_note is not None
    assert study_material.meaning_synonyms is not None
    assert study_material.hidden is not None


def test_all_reviews_parameters_are_imported(requests_mock):
    mock_reviews(requests_mock)
    client = Client("whatever")
    reviews = client.reviews()
    review = reviews[0]
    assert review.id is not None
    assert review.url is not None
    assert review.created_at is not None
    assert review.assignment_id is not None
    assert review.subject_id is not None
    assert review.starting_srs_stage is not None
    assert review.ending_srs_stage is not None
    assert review.starting_srs_stage_name is not None
    assert review.ending_srs_stage_name is not None
    assert review.incorrect_meaning_answers is not None
    assert review.incorrect_reading_answers is not None
