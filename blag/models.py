from . import db
from .blocks import render_blocks

from flask import Markup, url_for
from flask_wtf import Form
from sqlalchemy_defaults import Column
from wtforms_alchemy import model_form_factory, ModelFieldList
from wtforms.fields import FormField, HiddenField

import ujson as json

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

    slug = Column(
        db.String(40),
        info={'label': 'Slug'},
        nullable=False,
    )

    rendered_content = Column(
        db.Text,
    )

    raw_content = Column(
        db.Text,
        info={'label': 'Article'},
    )

    datetime_added = Column(
        db.DateTime,
        auto_now=True,
    )

    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

    def render(self):
        self.rendered_content = render_blocks(json.loads(self.raw_content)['data'])

    def url(self, external=False):
        year = self.datetime_added.year
        return url_for('blag.post_details', year=year, slug=self.slug, _external=external)


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
                fields.append('%s: %s' % (f.label, f()))
        return Markup('\n'.join(fields))



class BlogPostForm(_PrintableForm):
    class Meta(object):
        model = BlogPost
        only = [
            'title',
            'slug',
            'raw_content',
        ]
    def get_categories_query():
        return Tag.query.all()

    #tags = QuerySelectMultipleField(query_factory=get_categories_query)
    tags = ModelFieldList(FormField(TagForm))
