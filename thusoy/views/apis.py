from birdy.twitter import AppClient
from flask import Blueprint, current_app, Response, request

import requests
import ujson as json

mod = Blueprint(__name__, 'thusoy.apis')

@mod.route('/tweets/<tweet_id>')
def tweet(tweet_id):
    client = AppClient(
        current_app.config['TWITTER_CLIENT_ID'],
        current_app.config['TWITTER_CLIENT_SECRET'],
    )
    client.get_access_token()
    resource = client.api.statuses.show
    response = resource.get(id=tweet_id)
    data = json.dumps(response.data)
    return Response(data, mimetype='application/json')
