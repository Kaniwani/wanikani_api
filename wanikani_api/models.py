import dateutil.parser

from wanikani_api import constants


class Resource:
    def __init__(self, json_data):
        self.resource = json_data["object"]
        self.url = json_data["url"]
        self.data_updated_at = dateutil.parser.parse(json_data["data_updated_at"])
        # Some Resources do not have IDs.
        self.id = None if self.resource in constants.RESOURCES_WITHOUT_IDS else json_data["id"]
        self._raw_data = json_data["data"]

class Collection(Resource):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.next_page_url = json_data["pages"]["next_url"]
        self.previous_page_url = json_data["pages"]["previous_url"]
        self.items_per_page = json_data["pages"]["per_page"]
        self.total_count = json_data["total_count"]

class User(Resource):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.username = self._raw_data["username"]
        self.level = self._raw_data["level"]
        self.max_level_granted_by_subscription = self._raw_data["max_level_granted_by_subscription"]
        self.profile_url = self._raw_data["profile_url"]
        self.started_at = dateutil.parser.parse(self._raw_data["started_at"])
        self.subscribed = self._raw_data["subscribed"]
        self.current_vacation_started_at = dateutil.parser.parse(self._raw_data["started_at"])

