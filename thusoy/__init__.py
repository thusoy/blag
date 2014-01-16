from flask import Flask, send_from_directory, request
from flask.ext.sqlalchemy import SQLAlchemy
from jinja2 import FileSystemLoader
from logging import getLogger
from os import path
from sqlalchemy_defaults import make_lazy_configured

import logging.config
import os
import sqlalchemy
import textwrap
import ujson as json
import yaml

make_lazy_configured(sqlalchemy.orm.mapper)

db = SQLAlchemy()
_logger = getLogger('blag')


def create_app(**extra_config):
    app = Flask('thusoy')
    _configure_app(app, **extra_config)
    _init_logging(app)

    # register extensions
    db.init_app(app)


    jinja_loader = FileSystemLoader(path.join(path.dirname(__file__), loader_path) for loader_path in [
        'templates',
        'server-assets',
    ])
    app.jinja_loader = jinja_loader

    from .views import blog
    from .views import apis

    # Register blueprints
    app.register_blueprint(blog.mod)
    app.register_blueprint(apis.mod)


    with app.test_request_context():
        db.create_all()

    from . import context_processors

    app.context_processor(context_processors.default)
    app.context_processor(context_processors.config)
    app.context_processor(context_processors.revved_url_for)

    @app.errorhandler(500)
    def server_error(error):
        generic_error_handler(error)
        return 'Oops', 500

    @app.route('/images/<filename>')
    def images(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    if app.config['DEBUG']:
        # remove the default static url mapping
        for rule in app.url_map.iter_rules(endpoint='static'):
            del app.url_map._rules[app.url_map._rules.index(rule)]
        @app.route('/static/libs/<path:filename>')
        def libstatic(filename):
            return send_from_directory(path.join(path.dirname(__file__), 'static', 'libs'), filename)
        @app.route('/static/<path:filename>')
        def devstatic(filename):
            return send_from_directory(app.config['STATIC_FILES'], filename)
    return app


def _configure_app(app, **extra_config):
    # Load the core settings:
    core_settings = path.join(path.dirname(__file__), 'settings.py')
    app.config.from_pyfile(core_settings)

    # Load stuff from local config:
    config_from_environ = os.environ.get('THUSOY_CONFIG_FILE')
    if config_from_environ:
        app.config.from_pyfile(config_from_environ)

    # Override the config with anything set directly in the creation call:
    app.config.update(extra_config)

    # Set filerevisions
    with app.open_resource(path.join('server-assets', 'filerevs.json')) as filerevs_fh:
        filerevs = json.load(filerevs_fh)
        app.config.setdefault('filerevs', {}).update(filerevs)



def _init_logging(app):
    log_config_dest = app.config['LOG_CONF_PATH']
    with open(log_config_dest) as log_config_file:
        logging.config.dictConfig(yaml.load(log_config_file))


def generic_error_handler(exception):
    """ Log exception to the standard logger. """
    log_msg = textwrap.dedent("""Error occured!
        Path:                 %s
        Params:               %s
        HTTP Method:          %s
        Client IP Address:    %s
        User Agent:           %s
        User Platform:        %s
        User Browser:         %s
        User Browser Version: %s
        HTTP Headers:         %s
        Exception:            %s
        """ % (
            request.path,
            request.values,
            request.method,
            request.remote_addr,
            request.user_agent.string,
            request.user_agent.platform,
            request.user_agent.browser,
            request.user_agent.version,
            request.headers,
            exception
        )
    )
    _logger.exception(log_msg)
