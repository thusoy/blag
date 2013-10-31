#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from os import path

setup(
    name='thusoy-blag',
    version='0.1.0',
    author='Tarjei Husøy',
    author_email='tarjei@roms.no',
    url='https://github.com/thusoy/blag',
    description='Somewhere to ramble',
    packages=find_packages(),
    package_data={
        '': [
            path.join('templates', '*.html'),
            path.join('templates', '*', '*.html'),
            'log_conf.yaml',
        ],
    },
    zip_safe=False,
)
