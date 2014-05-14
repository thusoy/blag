"""
    Configuration of the devserver.
"""

from os import path, environ

DEBUG = True

SECRET_KEY = 'supersecret'

DEBUG_TB_ENABLED = False

DEBUG_TB_PROFILER_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'

UPLOAD_FOLDER = path.abspath('images')

STATIC_FILES = path.abspath(path.join('.tmp', 'static'))

LOG_CONF_PATH = path.abspath('dev_log_conf.yaml')

TWITTER_CLIENT_ID = environ['BLAG_TWITTER_CLIENT_ID']

TWITTER_CLIENT_SECRET = environ['BLAG_TWITTER_CLIENT_SECRET']
