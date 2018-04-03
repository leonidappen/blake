from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
	jwt_refresh_token_required,
	create_access_token,
	create_refresh_token,
	unset_jwt_cookies,
	set_access_cookies,
	set_refresh_cookies,
	get_csrf_token
)

from app.extensions import jwt
from app.models import User


blueprint = Blueprint("token", __name__)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
	return User.query.filter_by(username=identity).one_or_none()


@jwt.user_claims_loader
def add_claims_to_access_token(user):
	return {
	    "id": user.id,
		"username": user.username,
	    "email": user.email,
	}


@jwt.user_identity_loader
def user_identity_lookup(user):
	return user.username


@blueprint.route("/login", methods=["POST"])
def login():
	data = request.get_json(force=True)

	username = data.get('username', None)
	if not username:
		return jsonify({"error": "Missing username parameter"}), 400

	password = data.get('password', None)
	if not password:
		return jsonify({"error": "Missing password parameter"}), 400

	user = User.query.filter_by(username=username).one_or_none()

	if user:
		if user.verify_password(password):
			access_token = create_access_token(identity=user)
			refresh_token = create_refresh_token(identity=user)

			resp = jsonify({
				"access_csrf": get_csrf_token(access_token),
				"refresh_csrf": get_csrf_token(refresh_token)
			})
			
			set_access_cookies(resp, access_token)
			set_refresh_cookies(resp, refresh_token)
			
			return resp, 200

	return jsonify({"error": "Invalid username or password."}), 401


@blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
	current_user = get_jwt_identity()
	access_token = create_access_token(identity=current_user)
	resp = jsonify({'refresh': True})
	set_access_cookies(resp, access_token)
	return resp, 200


@blueprint.route("/logout", methods=["POST"])
def logout():
	resp = jsonify({'logout': True})
	unset_jwt_cookies(resp)
	return resp, 200
