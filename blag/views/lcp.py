import ujson as json

from flask import (Blueprint, current_app, Response, request, render_template,
    jsonify, redirect, url_for, abort)
from flask_login import login_required

from .. import db
from ..auth import admin_permission
from ..models import Hike, HikeDestination

mod = Blueprint('lcp', __name__)

@mod.route('/lcp')
def lcp():
    return render_template('lcp.html')


@mod.route('/lcp/peaks')
def lcp_peaks():
    peaks = HikeDestination.query.filter_by(is_summit=True)
    serialized = [peak.to_json() for peak in peaks]
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
    coordinates = request.form.get('coordinates') or abort(400)
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
    return render_template('lcp_destination.html')
