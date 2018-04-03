from flask import Flask

from app import commands, main, token
from app.settings import config
from app.extensions import db, migrate, jwt, cors, celery


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	register_extensions(app)
	register_blueprints(app)
	register_commands(app)

	return app


def register_extensions(app):
	db.init_app(app)
	migrate.init_app(app, db)
	jwt.init_app(app)
	cors.init_app(app,
		headers=["Content-Type","Authorization"],
		supports_credentials=True
	)
	celery.conf.update(app.config)


def register_blueprints(app):
	app.register_blueprint(main.blueprint)
	app.register_blueprint(token.blueprint, url_prefix="/token")


def register_commands(app):
	app.cli.add_command(commands.user)
	app.cli.add_command(commands.role)
	app.cli.add_command(commands.celery)