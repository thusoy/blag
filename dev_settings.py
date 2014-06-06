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

LOCAL_UPLOAD_DIR = path.abspath('images')

STATIC_FILES = path.abspath(path.join('.tmp', 'static'))

LOG_CONF_PATH = path.abspath('dev_log_conf.yaml')

TWITTER_CLIENT_SECRET = environ['BLAG_TWITTER_CLIENT_SECRET']

FACEBOOK_CONSUMER_SECRET = environ['FACEBOOK_SECRET']

FILESERVER_URL = 'login.stud.ntnu.no'
FILESERVER_USERNAME = 'tarjeikl'
FILESERVER_KEY_FILE = path.join(path.dirname(__file__), 'fileserver_key.key')
FILESERVER_MEDIA_DIR = '/home/shomec/t/tarjeikl/public_html/media/'

CELERY_BROKER_URL = 'amqp://'

MEDIA_URL = 'http://folk.ntnu.no/tarjeikl/media/'
