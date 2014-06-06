from flask import Blueprint, render_template

mod = Blueprint('pages', __name__)

@mod.route('/about')
def about():
    return render_template('me.html')


@mod.route('/projects')
def projects():
    return render_template('projects.html')
