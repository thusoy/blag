"""
    Configuration of the devserver.
"""

from os import path, environ

DEBUG = True

SECRET_KEY = 'supersecret'

DEBUG_TB_ENABLED = False

DEBUG_TB_PROFILER_ENABLED = True

SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL',
    'postgresql://vagrant:vagrant@10.20.30.50/vagrant?connect_timeout=2')

UPLOAD_FOLDER = path.abspath('images')

STATIC_FILES = path.abspath(path.join('.tmp', 'static'))

LOG_CONF_PATH = path.abspath('dev_log_conf.yaml')

TWITTER_CLIENT_SECRET = environ['BLAG_TWITTER_CLIENT_SECRET']

PORRIDGE_SECRETS = 'devkey:devsecret'

THUNDERFOREST_API_KEY = environ['THUNDERFOREST_API_KEY']
