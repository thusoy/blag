import os

import mock

from .. import create_app, db


def test_init_from_envvars():
    test_environ = {
        'BLAG_SECRET_KEY': 'testsecret',
        'BLAG_PORRIDGE_SECRETS': '1:secret',
    }
    with mock.patch.dict(os.environ, test_environ):
        app = create_app()
    assert app.config['SECRET_KEY'] == 'testsecret'
