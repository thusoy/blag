from . import db, create_app
from .models import BlogPost

from flask_debugtoolbar import DebugToolbarExtension
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from logging import getLogger

app = create_app()
Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

_logger = getLogger('blag.utils')

@manager.command
def rerender_blogposts(id=None):
    with app.test_request_context():
        if id is not None:
            blogposts = [BlogPost.query.get(id)]
        else:
            blogposts = BlogPost.query.all()
        for blogpost in blogposts:
            blogpost.render()
            _logger.info('New rendered content for %d: %s', blogpost.id, blogpost.rendered_content)
            db.session.add(blogpost)


@manager.command
def devserver():
    DebugToolbarExtension(app)
    app.run(extra_files=[
        'dev_settings.py',
    ], host="0.0.0.0", port=80)


@manager.command
def init_db():
    with app.app_context():
        db.create_all()


def main(): # pragma: no cover
    """ Runs the manager.

    Target for setup.py entry point.
    """
    manager.run()
