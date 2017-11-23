import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='helpdesk',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD 2-Clause License',
    description='A simple Django based helpdesk ticketing site.',
    long_description=README,
    url='https://www.example.com/',
    author='Winston Cadwell',
    author_email='wcadwell@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: BSD 2-Clause License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
