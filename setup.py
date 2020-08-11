"""Setup file acamesh package
"""
# Import modules
# --------------
from setuptools import setup, find_packages
import os

# Get path of the package, where steup.py is located
here = os.path.abspath(os.path.dirname(__file__))

# Read the verison number
with open(os.path.join(here, 'VERSION')) as versionFile:
    version = versionFile.read().strip()

# Store the README.md file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    longDescription = f.read()

setup(
    # Project name
    name='acamesh',

    # Version from the version file
    version=version,

    # Short description
    description='Academic mesh generation package',

    # Long descriptionf from README.md
    long_description=longDescription,
    long_description_content_type='text/markdown',

    # Github url
    url='https://github.com/amcc1996/acamesh',

    # Authors
    author='António Manuel Couto Carneiro @CM2S, FEUP',
    author_email='amcc@fe.up.pt',

    # Classifiers (selected from https://pypi.org/classifiers/)
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        # Python version obtained with https://pypi.org/project/check-python-versions/
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
    ],


    # Python version compatibility
    python_requires='>=3.5, <3.9',
)
