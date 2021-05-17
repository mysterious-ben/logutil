import os
import pathlib

from setuptools import setup

PATH = pathlib.Path(__file__).parent
VERSION = os.getenv("VERSION", "dev")

setup(
    version=VERSION,
)
