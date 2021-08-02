"""Packaging setup file"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            "scidatalib = scidatalib.cli:cli",
        ]
    }
)
