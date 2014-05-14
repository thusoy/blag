from flask import current_app, url_for

def default():
    return {
        'debug': current_app.config.get('DEBUG', False),
    }


def config():
    return {
        'config': {}
    }


def _revved_url_for(endpoint, **values):
    if endpoint == 'static':
        original_filename = values.get('filename')
        if original_filename:
            revved_filename = current_app.config['filerevs'].get(original_filename)
            if revved_filename:
                del values['filename']
                return url_for(endpoint, filename=revved_filename, **values)
    return url_for(endpoint, **values)


def revved_url_for():
    return {
        'url_for': _revved_url_for,
    }
