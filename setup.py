"""
This is a setup.py script for py2app

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main_app.py']
DATA_FILES = ['icon.png']
OPTIONS = {
    'iconfile': 'icon.png',
    # Exclude problematic packages from modulegraph analysis to prevent recursion errors.
    'excludes': ['vtracer', 'together'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
