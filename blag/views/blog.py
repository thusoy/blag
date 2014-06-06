# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .. import db
from ..auth import admin_permission
from ..blocks import render_block
from ..models import BlogPost, BlogPostForm, TagForm, BlogImage

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, Response
from flask.ext.login import login_required
from jinja2.filters import do_striptags, do_truncate
from logging import getLogger
from os import path, mkdir
from werkzeug.contrib.atom import AtomFeed

import ujson as json
import json as _slow_json

mod = Blueprint('blag', __name__)

_logger = getLogger('blag.blog')

@mod.route('/')
def main():
    entries = BlogPost.query.order_by(BlogPost.datetime_added.desc()).all()
    return render_template('home.html', entries=entries)


@mod.route('/blog', methods=['GET', 'POST'])
@login_required
@admin_permission.require(403)
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
    return render_template('new_entry.html', form=form), 200 if request.method == 'GET' else 400


@mod.route('/blag/<int:post_id>')
def post_details(post_id):
    post = BlogPost.query.get_or_404(post_id)
    description = do_truncate(do_striptags(post.rendered_content))
    title = post.title
    return render_template('post_details.html', post=post, description=description, title=title)


@mod.route('/blag/<int:post_id>/edit', methods=('GET', 'POST'))
@login_required
@admin_permission.require(403)
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        post.render()
        flash('Post modified successfully', 'success')
        return redirect(url_for('.post_details', post_id=post.id))
    return render_template('edit_entry.html', form=form, post=post)


@mod.route('/blag/<int:post_id>', methods=['DELETE'])
@login_required
@admin_permission.require(403)
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    return 'Post deleted', 200


@mod.route('/images', methods=['POST'])
@login_required
@admin_permission.require(403)
def image_upload():
    from ..tasks import upload_image_to_fileserver # avoids circular import issues
    _logger.info('Uploading image locally')
    data = json.loads(request.form.get('data'))
    file = request.files['attachment[file]']
    upload_dir = current_app.config['LOCAL_UPLOAD_DIR']
    image = BlogImage(alt_text=data.get('altText'), extension=path.splitext(file.filename)[1])
    db.session.add(image)
    db.session.commit()
    if not path.exists(upload_dir):
        mkdir(upload_dir)
    filename = '%d.%s' % (image.id, file.filename.split('.')[-1])
    file.save(path.join(upload_dir, filename))
    _logger.info('Image saved, spawning upload task')
    upload_image_to_fileserver.delay(image.id)
    _logger.info('Task spawned')
    return Response(json.dumps({
        'msg': 'Image upload OK',
        'imageUrl': image.orig_url,
    }), mimetype='application/json')


@mod.route('/styleguide')
def styleguide():
    blocks = [
        {
            "type": "text",
            "data": {
                "text": "# This is the first header\n\nThis is a normal text block.\n\n\n\nIt might contain several paragraphs, and should in general contain lots of markdown-formatted text.\n\n"
            }
        },
        {
            "type": "quote",
            "data": {
                "text": "> This is a short quote.",
                "cite": "Tarjei Husøy"
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
                "text": "> This is a quote consisting of several paragraphs.\n> \n> Just because some people saylots of sensible things.\n",
                "cite": "Everyone"
            }
        },
        {
            "type": "ul",
            "data": {
                "text":" - Bulletpoint 1\n - Bulletpoint 2\n - List are effing awesome\n"
            }
        },
        {
            "type": "code",
            "data": {
                "language": "python",
                "text": "# This is a code example:\n#!/usr/bin/env python\napp = Flask(__name__)\n\n@app.route(\'/\')\ndef home():\n    return render_template(\'home.html\')\n"
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
                "source": "https://suonto.com/"
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

    ]
    def pprint(block):
        return _slow_json.dumps(block, indent=4)
    return render_template('styleguide.html', blocks=blocks, pprint=pprint, render_block=render_block)


@mod.route('/blag.atom')
def blag_feed():
    feed = AtomFeed('Tarjei Husøy’s blag',
                    feed_url=request.url, url=request.url_root, author='Tarjei Husøy',
                    icon=url_for('static', filename='img/atom_icon.jpg', _external=True),
                    logo=url_for('static', filename='img/atom_logo.jpg', _external=True))
    articles = BlogPost.query.order_by(BlogPost.datetime_added.desc()).limit(15).all()
    for article in articles:
        feed.add(article.title, unicode(article.rendered_content),
                 content_type='html',
                 url=url_for('.post_details', post_id=article.id, _external=True),
                 updated=article.datetime_added,
                 published=article.datetime_added)
    return feed.get_response()
