from flask import Flask, send_from_directory, request, g, current_app
from flask_login import LoginManager, current_user
from flask_principal import Principal, identity_changed, Identity
from flask_sqlalchemy import SQLAlchemy
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

from ._flask_porridge import Porridge

make_lazy_configured(sqlalchemy.orm.mapper)

db = SQLAlchemy()
login_manager = LoginManager()
principal = Principal()
porridge = Porridge()

_logger = getLogger('blag')

def create_app(**extra_config):
    app = Flask('blag')
    _configure_app(app, **extra_config)
    _init_logging(app)

    # register extensions
    db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)
    porridge.init_app(app)

    # Set up login stuff
    from .auth import load_user
    login_manager.user_loader(load_user)

    # Include server-assets in the jinja loader
    jinja_loader = FileSystemLoader(path.join(path.dirname(__file__), loader_path) for loader_path in [
        'templates',
        'server-assets',
    ])
    app.jinja_loader = jinja_loader


    from .views import blog
    from .views import apis
    from .views import misc
    from .views import lcp
    from .auth.views import mod as auth_mod

    # Register blueprints
    app.register_blueprint(blog.mod)
    app.register_blueprint(apis.mod)
    app.register_blueprint(auth_mod)
    app.register_blueprint(misc.mod)
    app.register_blueprint(lcp.mod)

    @app.before_request
    def add_user():
        g.user = current_user
        if current_user.is_authenticated:
            identity_changed.send(current_app._get_current_object(), identity=Identity(current_user.id))

    from . import context_processors

    app.context_processor(context_processors.default)
    app.context_processor(context_processors.config)
    app.context_processor(context_processors.revved_url_for)

    @app.errorhandler(500)
    def server_error(error):
        generic_error_handler(error)
        return 'Oops', 500

    @app.errorhandler(403)
    def forbidden(error):
        return "Your kung-foo is insufficient to do this.", 403

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


def _configure_app(app, **extra_config):
    # Load the core settings:
    core_settings = path.join(path.abspath(path.dirname(__file__)), 'settings.py')
    app.config.from_pyfile(core_settings)

    # Load from envvars (needed for Heroku-like environments)
    for key, val in os.environ.items():
        if not key.startswith('BLAG_'):
            continue

        key = key[len('BLAG_'):]
        if val.lower() in ('t', 'true'):
            val = True
        elif val.lower() in ('f', 'false'):
            val = False

        try:
            val = int(val)
        except:
            pass

        print('Setting %s = %s' % (key, val))
        app.config[key] = val

    # Load stuff from local config:
    config_from_environ = os.environ.get('BLAG_CONFIG_FILE')
    if config_from_environ:
        print('Loading config from %s' % config_from_environ)
        app.config.from_pyfile(path.join(os.getcwd(), config_from_environ))

    # Override the config with anything set directly in the creation call:
    app.config.update(extra_config)

    # Set filerevisions
    filerevs_path = path.join('server-assets', 'filerevs.json')
    try:
        with app.open_resource(filerevs_path) as filerevs_fh:
            filerevs = json.load(filerevs_fh)
            app.config['FILEREVS'] = filerevs
    except IOError:
        print('No filerevs found, continuing without')
        app.config['FILEREVS'] = {}


def _init_logging(app):
    log_config_dest = app.config.get('LOG_CONF_PATH')
    if log_config_dest:
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
