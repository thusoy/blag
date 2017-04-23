from flask import current_app
from porridge import Porridge as _Porridge

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
from flask import _app_ctx_stack as stack


class Porridge(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)


    def init_app(self, app):
        secrets = app.config['PORRIDGE_SECRETS']
        porridge = _Porridge(secrets)
        app.config.setdefault('_PORRIDGE_INSTANCE', porridge)


    def boil(self, password):
        return self._instance.boil(password)


    def verify(self, password, encoded):
        return self._instance.verify(password, encoded)


    def needs_update(self, encoded):
        return self._instance.needs_update(encoded)


    @property
    def _instance(self):
        return current_app.config['_PORRIDGE_INSTANCE']
