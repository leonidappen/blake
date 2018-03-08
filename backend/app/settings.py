class Config:
	# Flask
	SECRET_KEY = "Meow"

	# Flask-SQLAlchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Flask-JWT-Extended
	JWT_SECRET_KEY = "Mew"


class ProdConfig(Config):
	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blake"


class StageConfig(Config):
	# Flask
	DEBUG = True

	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blake-stage"


config = {
	"prod": ProdConfig,
	"stage": StageConfig,
	"default": StageConfig
}
