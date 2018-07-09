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

This is how to retrieve all Subjects in Wanikani. Subjects are either :class:`.models.Kanji`, :class:`.models.Radical`, or :class:`.models.Vocabulary`.

.. code-block:: python

    >>> vocabulary = wk_api.subjects(types="vocabulary")
    >>> for vocab in vocabulary:
    >>>    print(vocab.readings[0].reading)
    "いち"
    "ひとつ"
    "なな"
    "ななつ"
    "きゅう"
    "ここのつ"
    ...
    >>> print(len(vocabulary))
    1000


Note that by default the client will only retrieve the first Page of results. This can be changed by passing ``fetch_all=True`` to any client function
which returns multiple results. Like so:

    >>> vocabulary = wk_api.subjects(types="vocabulary", fetch_all=True)
    >>> print(len(vocabulary))
    6301

Alternatively, if you decide afterwards you'd like to fill in the missing data, you can do this:

    >>> vocabulary = wk_api.subjects(types="vocabulary")
    >>> print(len(vocabulary))
    1000
    >>> vocabulary.fetch_all_pages()
    >>> print(len(vocabulary))
    6301

You are also free to fetch one page at a time. Note also that you can access indiviual :class:`.models.Page` objects if you like.

    >>> vocabulary = wk_api.subjects(types="vocabulary")
    >>> print(len(vocabulary))
    1000
    >>> vocabulary.fetch_next_page()
    >>> print(len(vocabulary))
    2000
    >>> print(len(vocabulary.pages))
    2
    # Iterate only over elements in the second page:
    >>> for vocab in vocabulary.pages[1]:
    >>>     print(vocab.parts_of_speech)
    ['noun', 'suru_verb']
    ['noun']
    ['intransitive_verb', 'godan_verb']

This works for any client function that is *plural*, e.g. assignments(), subjects(), reviews(), etc.

By default, the Wanikani API returns only subject IDs when referring to a subject. Therefore, for any resource which contains a field *subject_id* or *subject_ids* can make use of convenient properties *subject* and *subjects*, respectively.
This allows you to quickly grab related subjects without making a separate explicit call to the subjects endpoint. See below.

Assignments
___________
.. code-block:: python

    >>> assignments = wk_api.assignments(subject_types="vocabulary")
    >>> for assignment in assignments:
    >>>    print(assignment.srs_stage_name)
    >>>    print(assignment.subject.meaning) # The client will automatically go and fetch this subject for you.
    "Burned"
    "One"
    "Burned"
    "One Thing"


Note that the above will make a new API call every time you call ``subject`` on a new assignment.

Review Statistics
_________________

Here's how to get your review statistics for your level 30 vocabulary and kanji (but not radicals), that you have gotten correct at most 50%

.. code-block:: python

    >>> subjects = wk_api.subjects(types=["vocabulary", "kanji"], level=30)
    >>> stats = wk_api.review_statistics(subject_ids=[subject.id for subject in subjects], percentages_less_than=50)
    >>> for stat in stats:
    >>>     print(stat.percentage_correct)
    44
    42
    49
    31

Study Materials
_______________

Here's how to get all study materials for any vocabulary that have the slug　毛糸. The *slug* is a simple identifier on the wanikani site
(like this: https://www.wanikani.com/vocabulary/毛糸)

.. code-block:: python

    >>> subjects = wk_api.subjects(slugs="毛糸", types="vocabulary")
    >>> study_mats = wk_api.study_materials(subject_ids=[subject.id for subject in subjects])
    >>> for study_material in study_mats:
    >>> print (", ".join(study_material.meaning_synonyms)
    "wool,yarn"
