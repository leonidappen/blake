from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token

from app.extensions import jwt
from app.models import User


blueprint = Blueprint("auth", __name__, url_prefix="/auth")


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
	password = data.get('password', None)
	if not username:
		return make_response(jsonify({"error": "Missing username parameter"}), 400)
	if not password:
		return make_response(jsonify({"error": "Missing password parameter"}), 400)

	user = User.query.filter_by(username=username).one_or_none()

	if user:
		if user.verify_password(password):
			access_token = create_access_token(identity=user)
			return jsonify(access_token=access_token), 200

	return make_response(jsonify({"error": "Invalid username or password."}), 401)
