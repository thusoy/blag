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
FILESERVER_PUB_KEY = ('ssh-dss', 'AAAAB3NzaC1kc3MAAACBAL6nSvGlU3xVq+w4TmNilMn3L1jv+wfoj04lEiKvTfSVZLotgEXJT3R4TvA76BkSQ14mtNAilGXuFNjiL3BJ4VV3mi2kDk2jbto3sPnUFJhiLfAYEIjW0k2GMOa2hCO7b4ooK3Il0Kh70bWHioB75huTGRLO3C9bGXcSt8EryQgXAAAAFQDbt5i+eQiJ9WL1HDbuDMxWzADx0wAAAIBPzWlgGaNCAxa7C8P3obWI588gZIhEsFk2y8okCNFxn0tIehMU5ICK/Trgbfq29qQgfw1/MmoMGnidKImYas/9quV/4teNUyrOeRm0RLXLB57STBGJUGnkioVr5rgR9W0hFd3oeYolf+ZBXZ2HdlOWKysrmoXlViqq0+upUySj8QAAAIAksBNTdApDvjPuHhXGKuDuZMj+jBowTalIej8S+kGAlNzxxA6DTYLNxK7n0PrsJXZinDZux1/1eBIAZKp08v+uo8d+19Rh7PrslUfpc8kRzjwVe4QRb+7bmIy8iY6d99wGCB+c5W4rdz/fqFTReLO4Oiz3vd5uYs7RjuE31Pjz6Q==')

CELERY_BROKER_URL = 'amqp://'

MEDIA_URL = 'http://folk.ntnu.no/tarjeikl/media/'
