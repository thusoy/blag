from . import db, renderers

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
        raw_data = json.loads(self.raw_content)
        html_parts = []
        render_mapping = {
            'text': renderers.TextRenderer,
            'quote': renderers.QuoteRenderer,
            'image': renderers.ImageRenderer,
            'video': renderers.VideoRenderer,
            'gallery': renderers.GalleryRenderer,
            'tweet': renderers.TweetRenderer,
            'heading': renderers.HeadingRenderer,
            'sourced_quote': renderers.SourcedQuoteRenderer,
        }
        for part in raw_data['data']:
            renderer_class = render_mapping.get(part['type'], renderers.TextRenderer)
            renderer = renderer_class(part['data'])
            html_parts.append(renderer.render())
        self.rendered_content = ''.join(html_parts)


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
            'raw_content',
        ]
    def get_categories_query():
        return Tag.query.all()

    #tags = QuerySelectMultipleField(query_factory=get_categories_query)
    tags = ModelFieldList(FormField(TagForm))