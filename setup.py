#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="omelette",
    python_requires=">=3.6",
    version=get_version("omelette"),
    url="https://github.com/fespino/omelette",
    license="MIT",
    description="A LiveView implementation based on Starlette ASGI framework",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Francisco Espino",
    author_email="fespinoromero@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    package_data={"omelette": ["py.typed"]},
    include_package_data=True,
    extras_require={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    zip_safe=False,
)