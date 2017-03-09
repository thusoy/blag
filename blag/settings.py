"""
    blag.settings
    ~~~~~~~~~~~~~~~

    These are the core settings, which should not depend on the specific platform where the app is deployed.

    Settings that need to be configured on each platform is:

        * SECRET_KEY
        * SQLALCHEMY_DATABASE_URI
        * TWITTER_CLIENT_ID
        * TWITTER_CLIENT_SECRET

"""

SQLALCHEMY_COMMIT_ON_TEARDOWN = True

TWITTER_CLIENT_ID = '4lBdgu4J5FmxR2JfGnvA'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# There's no point in trying to hide this key as it's sent in the html to every
# browser anyway. Access is restricted with referer headers.
GOOGLE_MAPS_API_KEY = 'AIzaSyAGzz-huZj4m5nEEKhf_YkRaONyKA1zqSs'
