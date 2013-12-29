from flask import current_app

def default():
    return {
        'debug': current_app.config.get('DEBUG', False),
    }


def config():
    return {
        'config': {
            'GOOGLE_ANALYTICS_ID': current_app.config['GOOGLE_ANALYTICS_ID'],
        }
    }
