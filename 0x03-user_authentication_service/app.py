#!/usr/bin/env python3
"""Basic Flask app."""
from flask import Flask, jsonify, request, abort, redirect
from flask.helpers import make_response
from auth import Auth
from user import User
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def payload() -> str:
    """Return payload with message."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """Implement the POST /users route."""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Respond to the POST /sessions route."""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    message = make_response(jsonify({"email": email, "message": "logged in"}))
    message.set_cookie("session_id", session_id)
    return message


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Respond to the DELETE /sessions route."""
    cookies = request.cookies
    session_id = cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Respond to the GET /profile route."""
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Respond to the POST /reset_password route."""
    try:
        email = request.form['email']
        reset_token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)

    message = {"email": email, "reset_token": reset_token}

    return jsonify(message), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Respond to the PUT /reset_password route."""
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']

        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    message = {"email": email, "message": "Password updated"}
    return jsonify(message), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
