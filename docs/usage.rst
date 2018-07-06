.. highlight:: python

=====
Usage
=====
Getting a client
________________
.. code-block:: python

    >>> import wanikani_api.client as client
    >>> wk_api = client.Client("enter your V2 API key here")

User Information
________________
.. code-block:: python

    >>> import wanikani_api.client as client
    >>> wk_api = client.Client("enter your V2 API key here")
    >>> user_info = wk_api.user_information()
    >>> user.username
    "Tadgh"

Subjects
________
.. code-block:: python

    >>> vocabulary = client.subjects(types="vocabulary")
    >>> for vocab in vocabulary.data:
    >>>    print(vocab.readings[0].reading)

    "いち"
    "ひとつ"
    "なな"
    "ななつ"
    "きゅう"
    "ここのつ"
    ...

Assignments
___________
.. code-block:: python

    >>> vocabulary = client.assignments(types="vocabulary")
    >>> for vocab in vocabulary.data:
    >>>    print(vocab.readings[0].reading)
