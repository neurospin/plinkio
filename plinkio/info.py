#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Capsul current version
version_major = 0
version_minor = 1
version_micro = 1
version_extra = ""

# The following variables are here for backward compatibility in order to
# ease a transition for bv_maker users. They will be removed in a few days.
_version_major = version_major
_version_minor = version_minor
_version_micro = version_micro
_version_extra = version_extra

# Expected by setup.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}{3}".format(
    version_major, version_minor, version_micro, version_extra)

# Expected by setup.py: the status of the project
CLASSIFIERS = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities"]

# Project descriptions
description = "plinkio"
long_description = """
========
PLINKIO 
========

PLINK file I/O.
Started as utilities for imaging/genetics and shrinked down to a module for
PLINK I/O.
"""

# Dependencies
SPHINX_MIN_VERSION = 1.0

# Main setup parameters
NAME = "plinkio"
ORGANISATION = "CEA"
MAINTAINER = "Vincent Frouin"
MAINTAINER_EMAIL = "vincent.frouin@cea.fr"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/neurospin/plinkio.git"
DOWNLOAD_URL = "https://github.com/neurospin/plinkio.git"
LICENSE = "CeCILL-B"
CLASSIFIERS = CLASSIFIERS
AUTHOR = "PLINKIO developers"
AUTHOR_EMAIL = "vincent.frouin@cea.fr"
PLATFORMS = "OS Independent"
ISRELEASE = version_extra == ""
VERSION = __version__
PROVIDES = ["plinkio"]
REQUIRES = []
EXTRA_REQUIRES = {
    "doc": ["sphinx>=1.0"]
}
