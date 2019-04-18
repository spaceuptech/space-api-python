# https://realpython.com/pypi-publish-python-package
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="space-api-py",
    version="0.2.0",
    description="Space Cloud Client Python API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/spaceuptech/space-api-python",
    author="Space Up Tech",
    author_email="info@spaceuptech.com",
    license="Apache License, Version 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("test", "docs")),
    include_package_data=True,
    install_requires=["grpcio", "grpcio-tools", "protobuf"]
)