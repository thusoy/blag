from flask import Flask, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from logging import getLogger
from os import path
from sqlalchemy_defaults import make_lazy_configured

import logging.config
import sqlalchemy
import yaml


db = SQLAlchemy()
_logger = getLogger('thusoy')

def create_app(config_file=None, **extra_config):
    _init_logging()

    app = Flask(__name__)

    if config_file is not None:
        app.config.from_pyfile(config_file)
    app.config.update(extra_config)

    # register extensions
    db.init_app(app)

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
        _logger.exception("Something chrashed!")
        return 'Oops', 500

    @app.route('/images/<filename>')
    def images(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app


def _init_logging():
    log_config_dest = path.join(path.dirname(__file__), 'log_conf.yaml')
    with open(log_config_dest) as log_config_file:
        logging.config.dictConfig(yaml.load(log_config_file))
