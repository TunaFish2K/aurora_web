from flask import render_template
from flask_login import current_user
from . import main

@main.app_errorhandler(404)
def not_found(e):
    return render_template('404.html',user=current_user._get_current_object()),404

@main.app_errorhandler(500)
def inertal_server_error(e):
    return render_template('500.html',user=current_user._get_current_object()),500

@main.app_errorhandler(403)
def permission_denied(e):
    return render_template('403.html',user=current_user._get_current_object()),403