"""
    Configuration of the devserver.
"""

from os import path, environ

DEBUG = True

SECRET_KEY = 'supersecret'

DEBUG_TB_ENABLED = False

DEBUG_TB_PROFILER_ENABLED = True

# Don't use sqlite for migration, rely on postgres instead
SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'
#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/blag'

UPLOAD_FOLDER = path.abspath('images')

STATIC_FILES = path.abspath(path.join('.tmp', 'static'))

LOG_CONF_PATH = path.abspath('dev_log_conf.yaml')

TWITTER_CLIENT_SECRET = environ['BLAG_TWITTER_CLIENT_SECRET']

FACEBOOK_CONSUMER_SECRET = environ['FACEBOOK_SECRET']
