#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["requests", "python-dateutil"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Gary Grant Graham",
    author_email="gary@kaniwani.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="An API wrapper for Wanikani (V2)",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="wanikani_api",
    name="wanikani_api",
    packages=find_packages(include=["wanikani_api"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Kaniwani/wanikani_api",
    version="0.2.0",
    zip_safe=False,
)
