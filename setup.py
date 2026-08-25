"""Pyhton setup.py for embroi_link"""
import io
import os
from setuptools import find_packages, setup

def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name = "EmbroiLink",
    version = "1.0.0",
    description="Generating an embroidery design from an image",
    long_description=read("README.md"),
    url="https://github.com/SimonAdel26/EmbroiLink",
    packages=find_packages(),
    install_requires=read_requirements("requirements.txt"),
)