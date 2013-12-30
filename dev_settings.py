from os import path

DEBUG = True

SECRET_KEY = 'supersecret'

DEBUG_TB_ENABLED = False

DEBUG_TB_PROFILER_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'

UPLOAD_FOLDER = path.abspath('images')

STATIC_FILES = path.abspath(path.join('.tmp', 'thusoy', 'static'))

TWITTER_CLIENT_ID = 'XMqPL6EZV2hsmpZycMBf8g'

TWITTER_CLIENT_SECRET = 'A8rMzv7cCajNrAHDSdYQNtMeZtKNGGZwRXhbdIZXZo'

EMBEDLY_API_KEY = 'ab8ac2d9de4b448b950675ab4117471e'
