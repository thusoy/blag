import ujson as json

from flask import (Blueprint, current_app, Response, request, render_template,
    jsonify, redirect, url_for, abort)
from flask_login import login_required
from sqlalchemy.orm import contains_eager

from .. import db
from ..auth import admin_permission
from ..models import Hike, HikeDestination, HikeDestinationForm, HikeForm

mod = Blueprint('lcp', __name__)

@mod.route('/lcp')
def lcp():
    return render_template('lcp.html',
        google_maps_api_key=current_app.config['GOOGLE_MAPS_API_KEY'])


@mod.route('/lcp/peaks')
def lcp_peaks():
    hikes = Hike.query\
        .distinct(Hike.destination_id)\
        .join(Hike.destination)\
        .options(contains_eager(Hike.destination))\
        .filter(HikeDestination.is_summit==True)
    serialized = [hike.destination.to_json() for hike in hikes]
    return jsonify({
        'peaks': serialized,
    })


@mod.route('/lcp/destinations', methods=['POST'])
@login_required
@admin_permission.require(403)
def lcp_destinations():
    name = request.form.get('name') or abort(400)
    altitude = request.form.get('altitude') or abort(400)
    is_summit = 'is_summit' in request.form
    coordinates = request.form.get('high_point_coord') or abort(400)

    coordinates = coordinates.split(',')
    if not len(coordinates) == 2:
        abort(400)
    coordinates = [float(point) for point in coordinates]


    destination = HikeDestination(
        name=name,
        altitude=int(altitude),
        high_point_coord='POINT(%f %f)' % tuple(coordinates),
        is_summit=is_summit,
    )
    db.session.add(destination)
    return redirect(url_for('.lcp'))


@mod.route('/lcp/destinations')
@login_required
@admin_permission.require(403)
def lcp_destination_form():
    form = HikeDestinationForm()
    return render_template('lcp_destination.html', form=form)


@mod.route('/lcp/hikes', methods=['GET', 'POST'])
@login_required
@admin_permission.require(403)
def lcp_hikes():
    form = HikeForm()
    if form.validate_on_submit():
        hike = Hike()
        hform = HikeForm()
        hform.populate_obj(hike)
        # The ModelFieldList doesn't properly populate this field
        hike.destination_id = request.form['destination_id']
        db.session.add(hike)
        return redirect(url_for('.lcp'))
    return render_template('lcp_hike.html', form=form)
