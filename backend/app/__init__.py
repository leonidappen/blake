from flask import Flask

from app import commands, auth
from app.settings import config
from app.extensions import db, migrate, jwt, cors
from app.schemas import schema
from app.schemas.utils import GraphQLView


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	register_extensions(app)
	register_blueprints(app)
	register_commands(app)

	app.add_url_rule('/graphql',
		view_func=GraphQLView.as_view(
			'graphql',
			schema=schema,
			graphiql=True,
			context={
				"session": db.session
			}
		)
	)

	return app


def register_extensions(app):
	db.init_app(app)
	migrate.init_app(app, db)
	jwt.init_app(app)
	cors.init_app(app, headers=['Content-Type','Authorization'])


def register_blueprints(app):
	app.register_blueprint(auth.blueprint)


def register_commands(app):
	app.cli.add_command(commands.user)
	app.cli.add_command(commands.role)
