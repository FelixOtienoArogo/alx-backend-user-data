#!/usr/bin/env python3
"""Basic Flask app."""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
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
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    message = jsonify({"email": email, "message": "logged in"})
    message.set_cookie("session_id", session_id)
    return message


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
