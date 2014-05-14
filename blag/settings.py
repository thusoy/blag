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

TWEET_BASE_URL = 'http://api.twitter.com/1.1/stauses/show/'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
