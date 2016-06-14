from flask import Blueprint

mod = Blueprint('misc', __name__)

@mod.route('/robots.txt')
def robots_txt():
    headers = {
        'Cache-Control': 'public, max-age=600',
    }
    return 'User-agent: *\nDisallow: /\n', 200, headers

