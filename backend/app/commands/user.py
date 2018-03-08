import sys

import click
from flask.cli import with_appcontext

from app.models import User, Role
from app.extensions import db


@click.group()
def role():
	"""Roles misc"""
	pass

@role.command()
@click.option("--name", prompt="name", type=str)
@with_appcontext
def add(name):
	"""Add new Role to the database."""
	if Role.query.filter_by(name=name).all():
			sys.exit("Role already exists.")

	role = Role(name)
	db.session.add(role)
	db.session.commit()

	print("Role added successfully")


@click.group()
def user():
	"""Users misc"""
	pass

def validate_email(ctx, param, value):
	if not re.match(r"^[A-Za-z0-9\.\+_-]+@appen.com$", value):
		raise click.BadParameter("Should be a valid appen email. i.e. <user>@appen.com")
	return value

@user.command()
@click.option('--email', prompt='Email', type=str, callback=validate_email)
@click.password_option()
@with_appcontext
def add(email, password):
	"""Add new User to the database."""
	if User.query.filter_by(email=email).one_or_none():
		sys.exit("Email already in use.")

	user = User(email, password)
	db.session.add(user)
	db.session.commit()

	print("User added successfully")
