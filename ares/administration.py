from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import redirect, url_for, session, current_app, Blueprint, render_template, request, send_from_directory, send_file, make_response, render_template_string
from app import login_manager

admin = Blueprint('administration', __name__, url_prefix='/admin')

@admin.before_request
def ask_login():
  if not current_user.is_anonymous:
    return

  if getattr(current_app.view_functions[request.endpoint], 'no_login', False):
    return

  return redirect(url_for('ares.aresLogin', next=request.endpoint))