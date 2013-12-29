from os import path

DEBUG = True

SECRET_KEY = 'supersecret'

DEBUG_TB_ENABLED = False

DEBUG_TB_PROFILER_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True

UPLOAD_FOLDER = path.abspath('images')

TWEET_BASE_URL = 'http://api.twitter.com/1.1/stauses/show/'

TWITTER_CLIENT_ID = 'XMqPL6EZV2hsmpZycMBf8g'

TWITTER_CLIENT_SECRET = 'A8rMzv7cCajNrAHDSdYQNtMeZtKNGGZwRXhbdIZXZo'

EMBEDLY_API_KEY = 'ab8ac2d9de4b448b950675ab4117471e'

GOOGLE_ANALYTICS_ID = 'UA-18817203-1'
