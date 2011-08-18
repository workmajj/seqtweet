#!/usr/bin/env python

from setuptools import setup

setup(
    name="SeqTweet",
    version="0.1",
    author="John J. Workman",
    author_email="workman@alumni.duke.edu",
    url="https://github.com/workmajj/seqtweet",
    description="Stores arbitrary strings on Twitter by implementing linked \
        lists.",
    license = "BSD 3-Clause <http://www.opensource.org/licenses/BSD-3-Clause>",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Internet',
    ],
    install_requires=['Tweepy>=1.7.1'],
    packages=['seqtweet']
)
