#!/usr/bin/env python3
from setuptools import setup


def requirements(section=None):
    """Helper for loading dependencies from requirements files."""
    if section is None:
        filename = "requirements.txt"
    else:
        filename = f"requirements-{section}.txt"

    with open(filename) as file:
        return [line.strip() for line in file]


# See setup.cfg for the actual configuration.
setup(
    # setup needs to be able to import the library, for attr: to work
    setup_requires=requirements() + ['pytest-runner'],
    install_requires=requirements(),
    tests_require=requirements('tests'),
)
