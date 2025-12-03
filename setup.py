# setup.py
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="animation-recommender",
    version="0.1.0",
    author="Alvin",
    packages=find_packages(),        # discovers your packages
    install_requires=requirements,   # installs deps
    python_requires=">=3.9",
    include_package_data=True,
)
