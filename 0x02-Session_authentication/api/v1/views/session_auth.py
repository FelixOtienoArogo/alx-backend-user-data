#!/usr/bin/env python3
"""Flask view that handles all routes for the Session authentication."""
from werkzeug import exceptions
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request
from os import abort, environ, getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """POST /auth_session/login (= POST /api/v1/auth_session/login)."""
    user_email = request.form.get('email', None)
    user_pwd = request.form.get('password', None)

    if user_email is None or user_email == "":
        return jsonify({"error": "email missing"}), 400

    if user_pwd is None or user_pwd == "":
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": user_email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    session_name = getenv("SESSION_NAME")
    user_dict = jsonify(user.to_json())

    user_dict.set_cookie(session_name, session_id)
    return user_dict


@app_views.route(
        "/auth_session/logout",
        methods=['DELETE'],
        strict_slashes=False)
def session_logout() -> str:
    """DELETE /api/v1/auth_session/logout."""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
