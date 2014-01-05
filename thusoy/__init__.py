from flask import Flask, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from jinja2 import FileSystemLoader
from logging import getLogger
from os import path
from sqlalchemy_defaults import make_lazy_configured

import logging.config
import os
import sqlalchemy
import yaml


db = SQLAlchemy()
_logger = getLogger('thusoy')

def create_app(config_file=None, **extra_config):
    _init_logging()

    app = Flask('thusoy')

    core_settings = path.join(path.dirname(__file__), 'settings.py')
    app.config.from_pyfile(core_settings)

    if config_file is not None:
        app.config.from_pyfile(config_file)
    app.config.update(extra_config)
    config_from_environ = os.environ.get('THUSOY_CONFIG_FILE')
    if config_from_environ:
        app.config.from_pyfile(config_from_environ)

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

    make_lazy_configured(sqlalchemy.orm.mapper)

    with app.test_request_context():
        db.create_all()

    from . import context_processors

    app.context_processor(context_processors.default)
    app.context_processor(context_processors.config)

    @app.errorhandler(500)
    def server_error(error):
        _logger.exception("Something crashed!")
        return 'Oops', 500

    @app.route('/images/<filename>')
    def images(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    if app.config['DEBUG']:
        # remove the default static url mapping
        for rule in app.url_map.iter_rules(endpoint='static'):
            del app.url_map._rules[app.url_map._rules.index(rule)]
        @app.route('/static/<path:filename>')
        def devstatic(filename):
            return send_from_directory(app.config['STATIC_FILES'], filename)
    return app


def _init_logging():
    log_config_dest = path.abspath(path.join(path.dirname(__file__), 'log_conf.yaml'))
    with open(log_config_dest) as log_config_file:
        logging.config.dictConfig(yaml.load(log_config_file))
