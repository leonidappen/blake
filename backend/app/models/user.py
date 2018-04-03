from sqlalchemy import Table, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import backref, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .base import base, Base


user_roles = Table("user_roles",
	base.metadata,
	Column('user_id', Integer(), ForeignKey("users.id")),
	Column('role_id', Integer(), ForeignKey("roles.id"))
	)


class Role(Base):
	name = Column(Text, unique=True)

	def __init__(self, name):
		self.name = name


class User(Base):
	email = Column(Text, unique=True)
	username = Column(Text, unique=True)
	password_hash = Column(Text)
	roles = relationship('Role', secondary=user_roles,
							backref = backref('users', lazy='dynamic'))

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
