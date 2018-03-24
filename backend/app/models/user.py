from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from .base import Base


user_roles = db.Table("user_roles",
	db.Column('user_id', db.Integer(), db.ForeignKey("users.id")),
	db.Column('role_id', db.Integer(), db.ForeignKey("roles.id"))
	)


class Role(Base):
	name = db.Column(db.Text, unique=True)

	def __init__(self, name):
		self.name = name


class User(Base):
	email = db.Column(db.Text, unique=True)
	username = db.Column(db.Text, unique=True)
	password_hash = db.Column(db.Text)
	roles = db.relationship('Role', secondary=user_roles,
							backref = db.backref('users', lazy='dynamic'))

	def __init__(self, email, password):
		self.email = email
		self.username = email.split("@")[0]
		self.password = password

	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute.')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
