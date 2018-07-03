class InvalidWanikaniApiKeyException(Exception):
    """
    The client was initialized with an invalid V2 API key, causing
    Wanikani to return a ``401 unauthorized`` response.
    """

    pass


class UnknownResourceException(Exception):
    """
    The model factory was unable to determine what type of resource
    Wanikani is sending back, or is not familiar with it.
    """

    pass
