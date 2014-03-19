#!/usr/bin/python

from distutils.core import setup

setup(
    name="plinkio",
    version="0.1.0",
    description="PLINK file I/O",
    author="Vincent Frouin",
    author_email="vincent.frouin@cea.fr",
    packages=["plinkio",],
    long_description="""Started as utilities for imaging/genetics and
    shrinked down to a module for PLINK I/O""",
    classifiers=[])
