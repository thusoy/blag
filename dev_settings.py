"""
    Secrets that need to be declared in a file secrets.py:
        * TWITTER_CLIENT_ID
        * TWITTER_CLIENT_SECRET
"""


from .secrets import *

from os import path

DEBUG = True

SECRET_KEY = 'supersecret'

DEBUG_TB_ENABLED = False

DEBUG_TB_PROFILER_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'

UPLOAD_FOLDER = path.abspath('images')

STATIC_FILES = path.abspath(path.join('.tmp', 'static'))
