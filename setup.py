#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os


def package_files(directory, relative_to):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(path, filename)
            final_path = os.path.relpath(full_path, relative_to)
            paths.append(final_path)
    return paths

migration_files = package_files(os.path.join('blag', 'migrations'), os.path.abspath('blag'))
package_data = [
    os.path.join('templates', '*.html'),
    os.path.join('templates', '*', '*.html'),
    os.path.join('server-assets', '*'),
]

package_data.extend(migration_files)

setup(
    name='blag',
    version='0.1.0',
    author='Tarjei Husøy',
    author_email='git@thusoy.com',
    url='https://github.com/thusoy/blag',
    description='Somewhere to ramble',
    packages=find_packages(),
    package_data={
        '': package_data
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'manage.py = blag.scripts:main',
        ]
    }
)
