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

FACEBOOK_CONSUMER_ID = '403591906450053'
