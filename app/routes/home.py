# app/routes/home.py
from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.tasks'))
    return render_template('home.html')


@home_bp.route('/set-theme/<theme>')
def set_theme(theme):
    session['theme'] = theme
    return '', 204
