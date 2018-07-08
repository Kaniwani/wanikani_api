======================
|wk_logo| wanikani_api
======================

.. |wk_logo| image:: https://nihonamor.files.wordpress.com/2012/08/wanikani.png
        :target: https://wanikani.com
        :width: 56
        :height: 56
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

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
