from .. import db
from ..models import BlogPost, BlogPostForm, TagForm

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, Response
from logging import getLogger
from os import path
from werkzeug import secure_filename

import ujson as json

mod = Blueprint(__file__, 'blog')

_logger = getLogger('blag.blog')

@mod.route('/')
def main():
    entries = BlogPost.query.order_by(BlogPost.datetime_added.desc()).all()
    return render_template('home.html', entries=entries)


@mod.route('/blog', methods=['GET', 'POST'])
def new_post():
    _logger.debug(request.form)
    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost()
        form.populate_obj(post)
        post.render()
        db.session.add(post)
        flash("New entry saved!", 'success')
        return redirect(url_for('.main'))
    return render_template('new_entry.html', form=form), 400


@mod.route('/images', methods=['POST'])
def image_upload():
    _logger.info(request.data)
    _logger.info(request.files)
    file = request.files['attachment[file]']
    filename = secure_filename(file.filename)
    file.save(path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return Response(json.dumps({
        'msg': 'Image upload OK',
        'imageUrl': filename,
    }), mimetype='application/json')


@mod.route('/styleguide')
def styleguide():
    post = BlogPost()
    post.title = 'Styleguide'
    post.raw_content = u'''{
    "data": [
        {
            "type": "text",
            "data": {
                "text": "# This is the first header\\n\\nThis is a normal text block.\\n\\n\\n\\nIt might contain several paragraphs, and should in general contain lots of markdown-formatted text.\\n\\n"
            }
        },
        {
            "type": "quote",
            "data": {
                "text": "> This is a short quote.",
                "cite": "Tarjei Hus\xf8y"
            }
        },
        {
            "type": "text",
            "data": {
                "text": "This is some more text after the quote."
            }
        },
        {
            "type": "tweet",
            "data": {
                "user": {
                    "profile_image_url": "http://pbs.twimg.com/profile_images/3487712650/0d41ed3269413e459aa6f61b385e84e7_normal.jpeg",
                    "profile_image_url_https": "https://pbs.twimg.com/profile_images/3487712650/0d41ed3269413e459aa6f61b385e84e7_normal.jpeg",
                    "screen_name": "Susmumrik",
                    "name": "Susanne Egset"
                },
                "id": "396758841528156160",
                "text": "Religion is dead. #zombieapocalypse hit the #vatican http://t.co/OWHhvVdR5j",
                "created_at": "Sat Nov 02 22:00:53 +0000 2013",
                "status_url": "https://twitter.com/Susmumrik/status/396758841528156160"
            }
        },
        {
            "type": "heading",
            "data": {
                "text": "This is my heading"
            }
        },
        {
            "type": "quote",
            "data": {
                "text": "> This is a quote consisting of several paragraphs.\\n\\n> \\n\\n> Just because some people saylots of sensible things.\\n\\n",
                "cite": "Everyone"
            }
        },
        {
            "type": "ul",
            "data": {
                "text":" - Bulletpoint 1\\n - Bulletpoint 2\\n - List are effing awesome\\n"
            }
        },
        {
            "type": "text",
            "data": {
                "text": "This is a code example:\\n\\n\\n\\n    #/usr/bin/python\\n\\n    app = Flask(__name__)\\n\\n\\n\\n    @app.route(\'/\')\\n\\n    def home():\\n\\n        return render_template(\'home.html\')\\n\\n    \\n\\n"
            }
        },
        {
            "type": "text",
            "data": {
                "text": "This is vimeo video!"
            }
        },
        {
            "type": "video",
            "data": {
                "source": "vimeo",
                "remote_id": "48177187"
            }
        },
        {
            "type": "video",
            "data": {
                "source": "youtube",
                "remote_id": "Fq00mCqBMY8"
            }
        },
        {
            "type": "sourced_quote",
            "data": {
                "text": "Today has been crazy.",
                "author": "Markus",
                "source": "Markus.fi"
            }
        },
        {
            "type": "gallery",
            "data": [
                {
                    "type": "image",
                    "data": {
                        "msg": "Image upload OK",
                        "imageUrl": "DSC_0334.jpg"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "msg": "Image upload OK",
                        "imageUrl": "DSC_0333.jpg"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "msg": "Image upload OK",
                        "imageUrl": "DSC_0332.jpg"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "msg": "Image upload OK",
                        "imageUrl": "DSC_0331.jpg"
                    }
                }
            ]
        }

    ]}
    '''
    post.render()
    return render_template('home.html', entry=post)
