#!/usr/env/bin python
#-*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="xmind-sdk",
    version="0.1a0",
    author="Woody Ai",
    author_email="aiqi@xmind.net",
    description="The offical XMind python SDK",
    long_description=long_description,
    
    packages=find_packages(),

    install_requires=["distribute"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    license="MIT",
    keywords="XMind, SDK, mind mapping",
    python_requires='>=3.6',

    url="https://github.com/andrii-z4i/xmind-sdk-python.git",
    download_url='https://github.com/andrii-z4i/xmind-sdk-python/archive/v1.0.tar.gz',
)
