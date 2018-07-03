=====
Usage
=====

To use wanikani_api in a project::

    >>> import wanikani_api.client as client


To get a client::

    >>> wk_api = client.Client("enter your V2 API key here")

To query your user information:

    >>> user_info = wk_api.user_information()
    >>> user.username
    "Tadgh"

Subjects


