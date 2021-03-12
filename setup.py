"""Packaging setup file"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SciDataLib",
    version="0.1.0",
    author="Dylan Johnson, Stuart Chalk",
    author_email="n01448636@unf.edu, schalk@unf.edu",
    description="Python library for development of SciData JSON-LD files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChalkLab/SciDataLib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
