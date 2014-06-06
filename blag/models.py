#! -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import db
from .blocks import render_blocks

from flask import Markup, current_app
from flask.ext.wtf import Form
from sqlalchemy_defaults import Column
from wtforms_alchemy import model_form_factory, ModelFieldList
from wtforms.fields import FormField, HiddenField
import re
import ujson as json
import unicodedata


class ModelForm(model_form_factory(Form)):
    pass


tags = db.Table('tags',
    Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    Column('post_id', db.Integer, db.ForeignKey('blog_post.id')),
)


class Tag(db.Model):
    id = Column(
        db.Integer,
        primary_key=True,
    )

    name = Column(
        db.String(30),
        nullable=False,
        info={'label': 'Name'}
    )


class TagForm(ModelForm):
    class Meta(object):
        model = Tag
        only = [
            'name',
        ]


class BlogPost(db.Model):
    __lazy_options__ = {}

    id = Column(
        db.Integer,
        primary_key=True,
    )

    title = Column(
        db.String(40),
        info={'label': 'Title'},
    )

    rendered_content = Column(
        db.Text,
    )

    raw_content = Column(
        db.Text,
        info={'label': False},
    )

    datetime_added = Column(
        db.DateTime,
        auto_now=True,
    )

    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

    def render(self):
        self.rendered_content = render_blocks(json.loads(self.raw_content)['data'])


class _PrintableForm(model_form_factory(Form)):

    def render(self):
        fields = []
        for f in self:
            if isinstance(f, HiddenField):
                fields.append('<input type="hidden" name="%(name)s" value="%(value)s">' % {
                    'name': f.name,
                    'value': f._value(),
                })
            else:
                if f.label.text:
                    fields.append('%s: %s' % (f.label, f()))
                else:
                    fields.append(f())
        return Markup('\n'.join(fields))


class BlogPostForm(_PrintableForm):
    class Meta(object):
        model = BlogPost
        only = [
            'title',
            'raw_content',
        ]

    def get_categories_query():
        return Tag.query.all()

    #tags = QuerySelectMultipleField(query_factory=get_categories_query)
    tags = ModelFieldList(FormField(TagForm))


class BlogImage(db.Model):
    STATE_RECEIVED = 1
    STATE_RESIZED = 2
    STATE_READY = 3
    __lazy_options__ = {}

    id = Column(db.Integer, primary_key=True)
    extension = Column(db.String(10))
    alt_text = Column(db.Unicode(255))
    datetime_uploaded = Column(db.DateTime(), auto_now=True)
    slug = Column(db.String(255))
    state = Column(db.Integer, default=STATE_RECEIVED)

    def __init__(self, alt_text=None, slug=None, *args, **kwargs):
        if alt_text and not slug:
            slug = slugify(alt_text)
        return super(BlogImage, self).__init__(slug=slug, alt_text=alt_text, *args, **kwargs)


    @property
    def orig_url(self):
        return current_app.config['MEDIA_URL'] + self.orig_basepath


    @property
    def orig_basepath(self):
        return 'blag/images/%d/%s%s' % (self.datetime_uploaded.year, self.slug, self.extension)


class FileserverImage(db.Model):
    id = Column(db.Integer, primary_key=True)
    #: Filename relative to the app config `FILESERVER_MEDIA_DIR`
    filename = Column(db.String(255))
    height = Column(db.Integer, min=1)
    width = Column(db.Integer, min=1)

    @property
    def url(self):
        return current_app.config['MEDIA_URL'] + self.filename


    def delete(self):
        from .tasks import delete_from_fileserver
        delete_from_fileserver.delay(self.filename)


    def rename(self, new_filename):
        pass


def slugify(text):
    """ Make URL-friendly version of `text`. """
    text = text.replace('æ', 'ae').replace('ø', 'o').replace('å', 'a')
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub('[^\w\s-]', '', text).strip().lower()
    return re.sub('[-\s]+', '-', text)
