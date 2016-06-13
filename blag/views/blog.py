# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .. import db
from ..blocks import render_block
from ..context_processors import _revved_url_for as revved_url_for
from ..models import BlogPost, BlogPostForm, TagForm
from ..auth import admin_permission

from flask import (Blueprint, render_template, request, flash, redirect, url_for,
    current_app, Response, abort)
from flask_login import login_required
from jinja2.filters import do_striptags, do_truncate
from logging import getLogger
from os import path
from werkzeug import secure_filename
from werkzeug.contrib.atom import AtomFeed
from PIL import Image

import ujson as json
import json as _slow_json
import sqlalchemy as sa

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
    status_code = 200 if request.method == 'GET' else 400
    context = {
        'form': form,
        'async_stylesheets': [
            revved_url_for('static', filename='css/writeEntry.css'),
        ],
    }
    return render_template('new_entry.html', **context), status_code


@mod.route('/blag/<int(min=1, max=99):post_id>')
def post_details_old(post_id):
    # Redirect the old posts with just id-based lookups to slugs
    post = BlogPost.query.get_or_404(post_id)
    year = post.datetime_added.year
    return redirect(post.url())


@mod.route('/<int:year>/<slug>')
def post_details(year, slug):
    post = post_from_year_and_slug_or_404(year, slug)
    description = do_truncate(do_striptags(post.rendered_content))
    title = post.title
    return render_template('post_details.html', post=post, description=description, title=title)


def post_from_year_and_slug_or_404(year, slug):
    year_filter = sa.extract('year', BlogPost.datetime_added)
    post = BlogPost.query.filter(year_filter==year, BlogPost.slug==slug).first()
    if not post:
        abort(404)
    return post


@mod.route('/<int(min=1000, max=9999):year>')
def posts_in_year(year):
    year_filter = sa.extract('year', BlogPost.datetime_added)
    posts = BlogPost.query.filter(year_filter==year).all()
    return render_template('list_posts.html', posts=posts, year=year)


@mod.route('/<int(min=1000, max=9999):year>/<slug>/edit', methods=('GET', 'POST'))
@login_required
@admin_permission.require(403)
def edit_post(year, slug):
    post = post_from_year_and_slug_or_404(year, slug)
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        post.render()
        flash('Post modified successfully', 'success')
        return redirect(post.url())
    context = {
        'form': form,
        'post': post,
        'async_stylesheets': [
            revved_url_for('static', filename='css/writeEntry.css'),
        ],
    }
    return render_template('edit_entry.html', **context)


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
    _logger.info(request.data)
    _logger.info(request.files)
    file = request.files['attachment[file]']
    filename = secure_filename(file.filename)
    file_path = path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    data = {
        'path': url_for('images', filename=filename),
        'url': url_for('images', filename=filename),
        'name': filename,
    }
    try:
        data['dimensions'] = Image.open(file_path).size
    except:
        _logger.exception('Failed to get dimensions from image')
    return Response(json.dumps({
        'file': data,
        'msg': 'Image upload OK',
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
                 url=article.url(external=True),
                 updated=article.datetime_added,
                 published=article.datetime_added)
    return feed.get_response()
