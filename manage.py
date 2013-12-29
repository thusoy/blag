from thusoy import create_app, scripts

from flask.ext.script import Manager
from os import path



def main():
    config_file = path.abspath('dev_settings.py')
    app = create_app(config_file)
    manager = Manager(app)

    manager.add_command('devserver', scripts.Devserver())
    manager.add_command('rerender_blog_posts', scripts.RerenderBlogPosts())
    manager.run()

if __name__ == '__main__':
    main()
