import functools
import operator
import pprint

import dateutil.parser

from wanikani_api import constants
from wanikani_api.exceptions import UnknownResourceException


class Resource:
    def __init__(self, json_data, *args, **kwargs):
        self.resource = json_data["object"]
        self._raw = json_data
        self.url = json_data["url"]
        self.data_updated_at = parse8601(json_data["data_updated_at"])
        # Some Resources do not have IDs.
        self.id = (
            None
            if self.resource in constants.RESOURCES_WITHOUT_IDS
            else json_data["id"]
        )
        self._resource = json_data["data"]

    def raw_json(self):
        return pprint.pformat(self._raw)


class Iterator:
    def __init__(self, current_page, api_request, max_results=None, fetch_all=False):
        self.current_page = current_page
        self.api_request = api_request
        self.max_results = max_results
        self.yielded_count = 0
        self.pages = [current_page]
        if current_page:
            self.per_page = current_page.per_page
        if fetch_all:
            self.fetch_all_pages()

    def _keep_iterating(self):
        return (
            self.current_page is not None
            and self.max_results
            and self.yielded_count >= self.max_results
        )

    def fetch_next_page(self):
        if self.current_page.next_page_url is not None:
            self.pages.append(self.api_request(self.current_page.next_page_url))
            self.current_page = self.pages[-1]

    def fetch_all_pages(self):
        while self.current_page.next_page_url is not None:
            self.fetch_next_page()

    def __iter__(self):
        return iter([item for page in self.pages for item in page])

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.pages[item // self.per_page][item % self.per_page]
        if isinstance(item, slice):
            return [self[i] for i in range(*item.indices(len(self)))]

    def __len__(self):
        return functools.reduce(operator.add, [len(page) for page in self.pages])


class Page(Resource):
    resource = "collection"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.client = kwargs.get("client")
        self.next_page_url = json_data["pages"]["next_url"]
        self.previous_page_url = json_data["pages"]["previous_url"]
        self.total_count = json_data["total_count"]
        self.per_page = json_data["pages"]["per_page"]
        self.data = [factory(datum, client=self.client) for datum in json_data["data"]]

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.data[item]
        elif isinstance(item, slice):
            return [self.data[i] for i in range(*item.indices(len(self)))]

    def __len__(self):
        return len(self.data)


class Subjectable:
    """
    A Mixin allowing a model to quickly fetch related subjects.

    Any resource which inherits Subjectable must have either `subject_id` or `subject_ids` as an attribute.
    """

    def __init__(self, *args, **kwargs):
        if "client" not in kwargs:
            raise ValueError("Subjectable models expect an instance of Client!")
        self.client = kwargs.get("client")
        self._subjects = None
        self._subject = None

    @property
    def subject(self):
        if self._subject:
            return self._subject
        elif hasattr(self, "subject_id"):
            self._subject = self.client.subject(self.subject_id)
            return self._subject
        else:
            raise AttributeError("no attribute named subject!")

    @property
    def subjects(self):
        if self._subjects:
            return self._subjects
        elif hasattr(self, "subject_ids"):
            self._subjects = self.client.subjects(ids=self.subject_ids)
            return self._subjects
        else:
            raise AttributeError("no attribute named subjects!")


class Preferences():
    def __init__(self, preferences_json):
        self.default_voice_actor_id = preferences_json.get("default_voice_actor_id")
        self.lessons_batch_size= preferences_json["lessons_batch_size"]
        self.lessons_autoplay_audio = preferences_json["lessons_autoplay_audio"]
        self.reviews_autoplay_audio = preferences_json["reviews_autoplay_audio"]
        self.lessons_presentation_order = preferences_json["lessons_presentation_order"]
        self.reviews_display_srs_indicator = preferences_json["reviews_display_srs_indicator"]

class UserInformation(Resource):
    """
    This is a simple container for information returned from the ``/user/`` endpoint. This is all information related to
    the user.
    """

    resource = "user"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.username = self._resource["username"]  #: username
        self.level = self._resource["level"]  #: current wanikani level
        self.subscription = Subscription(self._resource['subscription']) #: maximum level granted by subscription.
        self.profile_url = self._resource["profile_url"]  #: Link to user's profile.
        self.started_at = parse8601(
            self._resource["started_at"]
        )  #: datetime at which the user signed up.
        self.current_vacation_started_at = parse8601(
            self._resource["current_vacation_started_at"]
        )  #: datetime at which vacation was enabled on wanikani.
        self.preferences = Preferences(self._resource["preferences"])

    def __str__(self):
        return "UserInformation{{ username:{}, level:{}, profile_url:{} started_at:{}, current_vacation_started_at:{} }}".format(
            self.username,
            self.level,
            self.profile_url,
            self.started_at,
            self.current_vacation_started_at,
        )


class Subject(Resource):
    """
    This is the base Subject for Wanikani. This contains information common to Kanji, Vocabulary, and Radicals.
    """

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        resource_data = json_data["data"]
        self.level = resource_data["level"]  #: The level of the subject.
        self.created_at = parse8601(
            resource_data["created_at"]
        )  #: The date at which the Subject was created originally on Wanikani.
        self.characters = resource_data[
            "characters"
        ]  #: The actual japanese kanji/radical symbol such as 女
        self.meanings = [
            Meaning(meaning_json) for meaning_json in resource_data["meanings"]
        ]  #: A list of :class:`.models.Meaning` for this subject.
        self.document_url = resource_data[
            "document_url"
        ]  #: The direct URL where the subject can be found on Wanikani
        self.hidden_at = resource_data[
            "hidden_at"
        ]  #: When Wanikani removes a subject, they seem to instead set it to hidden, for backwards compatibilty with clients.
        self.auxiliary_meanings = [
            AuxiliaryMeaning(auxiliary_meaning_json) for auxiliary_meaning_json in resource_data["auxiliary_meanings"]
        ]

    def __str__(self) -> str:
        return f"{['['+meaning.meaning+']' if meaning.primary else meaning.meaning for meaning in self.meanings]}:{[character for character in self.characters] if self.characters else 'UNAVAILABLE'}"


class Radical(Subject):
    """
    A model for the Radical object.
    """

    resource = "radical"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.character_images = (
            self._resource["character_images"]
            if "character_images" in self._resource.keys()
            else None
        )  #: A list of dictionaries, each containing a bunch of information related to a single character image.
        self.amalgamation_subject_ids = self._resource[
            "amalgamation_subject_ids"
        ]  #: IDs for various other :class:`.models.Subject` for which this radical is a component.

    def __str__(self) -> str:
        return f"Radical: {[meaning.meaning for meaning in self.meanings]}:{[character for character in self.characters] if self.characters else 'UNAVAILABLE'}"


class Vocabulary(Subject):
    """
    A model for the Vocabulary Resource
    """

    resource = "vocabulary"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.parts_of_speech = self._resource[
            "parts_of_speech"
        ]  #: A list of strings, each of which is a part of speech.
        self.component_subject_ids = self._resource[
            "component_subject_ids"
        ]  #: List of IDs for :class"`.models.Kanji` which make up this vocabulary.
        self.readings = [
            Reading(reading_json) for reading_json in self._resource["readings"]
        ]  #: A list of :class:`.models.Reading` related to this Vocabulary.

    def __str__(self):
        return f"Vocabulary: {super(Vocabulary, self).__str__()}"


class Kanji(Subject):
    """
    A model for the Kanji Resource
    """

    resource = "kanji"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.amalgamation_subject_ids = self._resource[
            "amalgamation_subject_ids"
        ]  #: A list of IDs for the related :class:`.models.Vocabulary` which this Kanji is a component in.
        self.component_subject_ids = self._resource[
            "component_subject_ids"
        ]  #: A list of IDs for the related :class:`.models.Radical` which combine to make this kanji
        self.readings = [
            Reading(reading_json) for reading_json in self._resource["readings"]
        ]  #: A list of :class:`.models.Reading` related to this Vocabulary.

    def __str__(self):
        return f"Kanji: {super(Kanji, self).__str__()}"

class AuxiliaryMeaning:
    """
    Simple data class for handling auxiliary meanings
    """
    def __init__(self, auxiliary_meaning_json):
        self.meaning = auxiliary_meaning_json["meaning"]
        self.type = auxiliary_meaning_json["type"]

    def __str__(self) -> str:
        return f"{self.meaning}({type})"

class Subscription:
    def __init__(self, subscription_json):
        self.active = subscription_json["active"]
        self.type = subscription_json["type"]
        self.max_level_granted = subscription_json["max_level_granted"]
        self.period_ends_at = parse8601(subscription_json["period_ends_at"])

    def __str__(self) -> str:
        return f"{'active' if self.active else 'inactive'}:{self.type}:{self.max_level_granted}:{self.period_ends_at}"

class Meaning:
    """
    Simple class holding information about a given meaning of a vocabulary/Kanji
    """

    def __init__(self, meaning_json):
        self.meaning = meaning_json["meaning"]  #: The english meaning of a Subject.
        self.primary = meaning_json[
            "primary"
        ]  #: Wether or not the meaning is considered to be the main one.
        self.accepted_answer = meaning_json[
            "accepted_answer"
        ]  #: Whether or not this answer is accepted during reviews in Wanikani.

    def __str__(self) -> str:
        return self.meaning


class Reading:
    """
    Simple class holding information about a given reading of a vocabulary/kanji
    """

    def __init__(self, meaning_json):
        #: the actual かな for the reading.
        self.reading = meaning_json["reading"]
        self.primary = meaning_json["primary"]  #: Whether this is the primary reading.
        self.accepted_answer = meaning_json[
            "accepted_answer"
        ]  #: Whether this answer is accepted as correct by Wanikani during review.


class Assignment(Resource, Subjectable):
    """
    Simple class holding information about Assignmetns.
    """

    resource = "assignment"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        Subjectable.__init__(self, *args, **kwargs)
        self.created_at = parse8601(self._resource["created_at"])
        self.subject_id = self._resource["subject_id"]
        self.subject_type = self._resource["subject_type"]
        self.srs_stage = self._resource["srs_stage"]
        self.srs_stage_name = self._resource["srs_stage_name"]
        self.unlocked_at = parse8601(self._resource["unlocked_at"])
        self.started_at = parse8601(self._resource["started_at"])
        self.passed_at = parse8601(self._resource["passed_at"])
        self.burned_at = parse8601(self._resource["burned_at"])
        self.available_at = parse8601(self._resource["available_at"])
        self.resurrected_at_at = parse8601(self._resource["resurrected_at"])
        self.passed = self._resource["passed"]
        self.hidden = self._resource["hidden"]


class Reset(Resource):
    """
    Simple model holding resource information
    """

    resource = "reset"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.created_at = parse8601(self._resource["created_at"])
        self.original_level = self._resource["original_level"]
        self.target_level = self._resource["target_level"]
        self.confirmed_at = parse8601(self._resource["confirmed_at"])


class ReviewStatistic(Resource):
    """
    Simple model holding ReviewStatistic Information
    """

    resource = "review_statistic"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.created_at = parse8601(self._resource["created_at"])
        self.subject_id = self._resource["subject_id"]
        self.subject_type = self._resource["subject_type"]
        self.meaning_correct = self._resource["meaning_correct"]
        self.meaning_incorrect = self._resource["meaning_incorrect"]
        self.meaning_max_streak = self._resource["meaning_max_streak"]
        self.meaning_current_streak = self._resource["meaning_current_streak"]
        self.reading_correct = self._resource["reading_correct"]
        self.reading_incorrect = self._resource["reading_incorrect"]
        self.reading_max_streak = self._resource["reading_max_streak"]
        self.reading_current_streak = self._resource["reading_current_streak"]
        self.percentage_correct = self._resource["percentage_correct"]
        self.hidden = self._resource["hidden"]


class StudyMaterial(Resource, Subjectable):
    """
    Simple model holding information about Study Materials
    """

    resource = "study_material"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        Subjectable.__init__(self, *args, **kwargs)
        self.created_at = parse8601(self._resource["created_at"])
        self.subject_id = self._resource["subject_id"]
        self.subject_type = self._resource["subject_type"]
        self.meaning_note = self._resource["meaning_note"]
        self.reading_note = self._resource["reading_note"]
        self.meaning_synonyms = self._resource["meaning_synonyms"]
        self.hidden = self._resource["hidden"]


class Lessons(object):
    def __init__(self, json_data, *args, **kwargs):
        self.subject_ids = json_data["subject_ids"]
        self.available_at = parse8601(json_data["available_at"])


class UpcomingReview(Subjectable):
    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        Subjectable.__init__(self, *args, **kwargs)
        self.subject_ids = json_data["subject_ids"]
        self.available_at = parse8601(json_data["available_at"])


class Summary(Resource):
    resource = "report"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.client = kwargs.get("client")
        # Note that there is only ever one lesson object, as per this forum thread https://community.wanikani.com/t/api-v2-alpha-documentation/18987
        self.lessons = Lessons(self._resource["lessons"][0])
        self.next_reviews_at = self._resource["next_reviews_at"]
        self.reviews = [
            UpcomingReview(review_json, client=self.client)
            for review_json in self._resource["reviews"]
        ]


class Review(Resource, Subjectable):
    resource = "review"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        Subjectable.__init__(self, *args, **kwargs)
        self.created_at = parse8601(self._resource["created_at"])
        self.assignment_id = self._resource["assignment_id"]
        self.subject_id = self._resource["subject_id"]
        self.starting_srs_stage = self._resource["starting_srs_stage"]
        self.starting_srs_stage_name = self._resource["starting_srs_stage_name"]
        self.ending_srs_stage = self._resource["ending_srs_stage"]
        self.ending_srs_stage_name = self._resource["ending_srs_stage_name"]
        self.incorrect_meaning_answers = self._resource["incorrect_meaning_answers"]
        self.incorrect_reading_answers = self._resource["incorrect_reading_answers"]


class LevelProgression(Resource):
    resource = "level_progression"

    def __init__(self, json_data, *args, **kwargs):
        super().__init__(json_data, *args, **kwargs)
        self.created_at = parse8601(self._resource["created_at"])
        self.level = self._resource["level"]
        self.unlocked_at = parse8601(self._resource["unlocked_at"])
        self.started_at = parse8601(self._resource["started_at"])
        self.passed_at = parse8601(self._resource["passed_at"])
        self.completed_at = parse8601(self._resource["completed_at"])


def parse8601(time_field):
    if time_field:
        return dateutil.parser.parse(time_field)
    else:
        return None


resources = {
    UserInformation.resource: UserInformation,
    Assignment.resource: Assignment,
    Review.resource: Review,
    ReviewStatistic.resource: ReviewStatistic,
    LevelProgression.resource: LevelProgression,
    StudyMaterial.resource: StudyMaterial,
    Reset.resource: Reset,
    Kanji.resource: Kanji,
    Vocabulary.resource: Vocabulary,
    Radical.resource: Radical,
    Summary.resource: Summary,
    Page.resource: Page,
}


def factory(resource_json, *args, **kwargs):
    try:
        return resources[resource_json["object"]](resource_json, *args, **kwargs)
    except KeyError:
        raise UnknownResourceException(
            "We have no clue how to handle resource of type: {}".format(
                resource_json["object"]
            )
        )
