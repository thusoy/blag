from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required
from ..auth import admin_permission
from .. import db
from ..models import MediaRecommendation, MediaRecommendationForm

mod = Blueprint('pages', __name__)

@mod.route('/about')
def about():
    return render_template('me.html')


@mod.route('/projects')
def projects():
    return render_template('projects.html')


@mod.route('/recommends')
def recommendations():
    recommendations = MediaRecommendation.query.all()
    context = {
        'recommendations': recommendations,
    }
    return render_template('recommendations.html', **context)


@mod.route('/recommends/new', methods=['GET', 'POST'])
# @login_required
# @admin_permission.require(403)
def new_recommendation():
    form = MediaRecommendationForm()
    if form.validate_on_submit():
        recommendation = MediaRecommendation()
        form.populate_obj(recommendation)
        db.session.add(recommendation)
        return redirect(url_for('.recommendations'))
    return render_template('new_recommendation.html', form=form)
