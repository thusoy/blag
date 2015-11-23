from . import db
from .blocks import render_blocks

from flask import Markup
from flask.ext.wtf import Form
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
                if not f.label.text:
                    f.label.text = f.name.title()
                fields.append('%s: %s' % (f.label, f()))
        return Markup('<br>'.join(fields))


class MediaRecommendation(db.Model):
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(255))
    credits = Column(db.String(255))
    medium = Column(db.String(255))
    href = Column(db.String(255), info={'label': 'Link'})
    description = Column(db.Text, default='')
    datetime_added = Column(db.DateTime, auto_now=True)


class MediaRecommendationForm(_PrintableForm):
    class Meta(object):
        model = MediaRecommendation
        only = (
            'title',
            'credits',
            'medium',
            'href',
            'description',
        )



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
