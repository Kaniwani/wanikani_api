======================
|wk_logo| wanikani_api
======================

.. |wk_logo| image:: https://discourse-cdn-sjc1.com/business5/uploads/wanikani_community/original/3X/7/a/7a2bd7e8dcf8d7766b51a77960d86949215c830c.png?v=5
        :target: https://wanikani.com
        :align: middle


.. image:: https://img.shields.io/pypi/v/wanikani_api.svg
        :target: https://pypi.python.org/pypi/wanikani_api

.. image:: https://img.shields.io/travis/Kaniwani/wanikani_api.svg
        :target: https://travis-ci.org/Kaniwani/wanikani_api

.. image:: https://readthedocs.org/projects/wanikani-api/badge/?version=latest
        :target: https://wanikani-api.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/Kaniwani/wanikani_api/shield.svg
     :target: https://pyup.io/repos/github/Kaniwani/wanikani_api/
     :alt: Updates


An API wrapper for Wanikani (V2)


* Free software: BSD license
* Documentation: https://wanikani-api.readthedocs.io.


Features
--------

* Easy access to Wanikani resources associated to your account.
* Automatic handling of pagination.
* Automatic fetching of related Subjects


Quickstart
----------

.. code-block:: python

    >>> from wanikani_api.client import Client
    >>> v2_api_key = "drop_your_v2_api_key_in_here" # You can get it here: https://www.wanikani.com/settings/account
    >>> client = Client(v2_api_key)
    >>> user_information = client.user_information()
    >>> print(user_information)
    UserInformation{ username:Tadgh11, level:8, max_level_granted_by_subscription:60, profile_url:https://www.wanikani.com/users/Tadgh11 started_at:2013-07-09 12:02:54.952786+00:00, subscribed:True, current_vacation_started_at:None }
    >>> all_vocabulary = client.subjects(types="vocabulary")
    >>> for vocab in all_vocabulary:
    >>>     print(vocab.meanings[0].meaning) #Vocabulary may have multiple meanings, we just grab the first in the list.
    One
    One Thing
    Seven
    Seven Things
    Nine
    Nine Things
    Two
    ...


TODO
----
* Make use of ETags for caching
* simplify API
* Improve automatic prefetching of subjects when relevant.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
