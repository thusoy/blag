# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .. import db
from ..blocks import render_block
from ..models import BlogPost, BlogPostForm, TagForm
from ..auth import admin_permission

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, Response
from flask.ext.login import login_required
from logging import getLogger
from os import path
from werkzeug import secure_filename

import ujson as json
import json as _slow_json
import datetime

mod = Blueprint(__file__, 'blog')

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
    return render_template('post_details.html', post=post)


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
