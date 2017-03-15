from . import db
from .blocks import render_blocks

from flask import Markup, url_for
from flask_wtf import Form
from geoalchemy2 import Geometry
from sqlalchemy_defaults import Column
from sqlalchemy_utils import ChoiceType
from sqlalchemy import func, CheckConstraint
from wtforms_alchemy import model_form_factory, ModelFieldList
from wtforms import FormField, HiddenField, TextField

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
        nullable=False,
    )

    raw_content = Column(
        db.Text,
        info={'label': 'Article'},
        nullable=False,
    )

    datetime_added = Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False,
    )

    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

    def render(self):
        self.rendered_content = render_blocks(json.loads(self.raw_content)['data'])

    def url(self, external=False):
        return url_for('blag.post_details', year=self.year, slug=self.slug, _external=external)

    @property
    def year(self):
        return self.datetime_added.year


class HikeDestination(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(100), nullable=False)
    altitude = Column(db.Integer, nullable=True) # TODO: Require if is_summit
    high_point_coord = Column(Geometry('POINT'), nullable=False,
        info={
            'form_field_class': TextField,
            # 'validators': CoordinateValidator(), # TODO: Ensure input is validated and casted to something understandable by PostGIS
        }
    ) # TODO: Require if summit
    is_summit = Column(db.Boolean, nullable=False, server_default='t')
    created_at = Column(db.DateTime, nullable=False, server_default=func.now())

    def to_json(self):
        geojson = json.loads(db.session.scalar(self.high_point_coord.ST_AsGeoJSON()))
        return {
            'name': self.name,
            'coordinates': geojson['coordinates'],
        }


    def __str__(self):
        return '%s (%d)' % (self.name, self.altitude)


class Hike(db.Model):
    __lazy_options__ = {}
    METHODS = [
        ('ski', 'Ski'),
        ('foot', 'Foot'),
        ('crampons', 'Crampons'),
        ('climb', 'Climb'),
        ('via ferrata', 'Via Ferrata'),
    ]
    id = Column(db.Integer, primary_key=True)
    destination_id = Column(db.Integer, db.ForeignKey(HikeDestination.id), nullable=False)
    destination = db.relationship(HikeDestination, backref=db.backref('hikes'))
    date = Column(db.Date, nullable=True, server_default=func.now())
    method = Column(ChoiceType(METHODS), nullable=False)
    notes = Column(db.Text, nullable=False, server_default='')
    created_at = Column(db.DateTime, nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint("method in (%s)" % ','.join("'%s'" % method[0] for method in METHODS)),
    )


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
                if isinstance(f, ModelFieldList):
                    # import pdb; pdb.set_trace()
                    for form_class in f.unbound_field.args:
                        fields.append(form_class().render_selector(f.name))
                else:
                    f.label.text = f.label.text or f.name.replace('_', ' ').title()
                    for error in f.errors:
                        fields.append('<span style="color:red">%s</span>' % error)
                    fields.append('%s: %s' % (f.label, f()))
        # TODO: Is this safe with user-submitted data on form edit?
        return Markup('\n'.join(fields))


    def render_selector(self, parent_field_name):
        alternatives = self.Meta.model.query.all()
        html = [
            '<select name="%s">' % parent_field_name,
        ]

        for alternative in alternatives:
            html.append('<option value="%s">%s</option>' % (alternative.id, alternative))

        html.append('</select>')
        return '\n'.join(html)


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


class HikeDestinationForm(_PrintableForm):
    class Meta(object):
        model = HikeDestination
        only = [
            'name',
            'altitude',
            'high_point_coord',
            'is_summit',
        ]


class HikeForm(_PrintableForm):
    class Meta(object):
        model = Hike
        only = [
            # 'destination_id',
            'method',
            'date',
        ]
    destination_id = ModelFieldList(FormField(HikeDestinationForm))
