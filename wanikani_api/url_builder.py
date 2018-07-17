import datetime


class UrlBuilder:
    def __init__(self, api_root):
        self.api_root = api_root

    def build_wk_url(self, endpoint, parameters=None, resource_id=None):
        if resource_id is not None:
            return "{0}{1}/{2}".format(self.api_root, endpoint, resource_id)
        else:
            parameter_string = self._build_query_parameters(parameters)
            return "{0}{1}{2}".format(self.api_root, endpoint, parameter_string)

    def _parse_parameter(self, parameter):
        key = parameter[0]
        value = parameter[1]
        if self._parameter_should_be_ignored(key, value):
            return None
        if isinstance(value, list):
            return "{}={}".format(key, ",".join(str(elem) for elem in value))
        elif isinstance(value, bool):
            return "{}={}".format(key, str(value).lower())
        elif isinstance(value, datetime.datetime):
            return "{}={}".format(key, value.isoformat())
        else:
            return "{}={}".format(key, str(value))

    def _parameter_should_be_ignored(self, key, value):
        return value is None or key in ["self", "resource_id", "fetch_all"]

    def _build_query_parameters(self, parameters):
        if parameters:
            query_parameters = list(
                map(self._parse_parameter, sorted(parameters.items()))
            )
            query_parameters = [qp for qp in query_parameters if qp is not None]
            if query_parameters:
                return "?{}".format("&".join(query_parameters))
        return ""
