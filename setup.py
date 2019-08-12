"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='conftl',
    version='0.4.0',
    description='Configuration Templating Language',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ttt-fifo/conftl',
    author='Todor Todorov',
    license='BSD',
    author_email='ttodorov@null.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords='templating configuration development sysadmin devops',
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    python_requires='>=2.7, <4',
    entry_points={
        'console_scripts': [
            'render=conftl.command_line:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/ttt-fifo/conftl/issues',
        'Source': 'https://github.com/ttt-fifo/conftl/',
    },
)
