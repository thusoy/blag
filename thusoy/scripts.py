from . import db, create_app
from .models import BlogPost

from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.script import Command, Option
from logging import getLogger
from os import path

_logger = getLogger('thusoy.utils')
_dev_settings = path.abspath('dev_settings.py')

class RerenderBlogPosts(Command):

    option_list = (
        Option('--id', dest='id'),
    )

    def run(self, id=None):
        app = create_app(config_file=_dev_settings)
        with app.test_request_context():
            if id is not None:
                blogposts = [BlogPost.query.get(id)]
            else:
                blogposts = BlogPost.query.all()
            for blogpost in blogposts:
                blogpost.render()
                _logger.info('New rendered content for %d: %s', blogpost.id, blogpost.rendered_content)
                db.session.add(blogpost)


class Devserver(Command):

    def run(self):
        app = create_app(config_file=_dev_settings)
        DebugToolbarExtension(app)
        app.run(extra_files=[
            'dev_settings.py',
        ], host="0.0.0.0")
