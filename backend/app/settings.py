class Config:
	# Flask
	SECRET_KEY = "Meow"

	# Flask-SQLAlchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Flask-JWT-Extended
	JWT_SECRET_KEY = "Mew"

	# Celery
	CELERYD_CONCURRENCY = 2


class ProdConfig(Config):
	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blake"

	# Celery
	BROKER_URL = "redis://localhost:6379/0"
	CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


class StageConfig(Config):
	# Flask
	DEBUG = True

	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blake-stage"

	# Celery
	BROKER_URL = "redis://localhost:6379/1"
	CELERY_RESULT_BACKEND = "redis://localhost:6379/1"


config = {
	"prod": ProdConfig,
	"stage": StageConfig,
	"default": StageConfig
}
