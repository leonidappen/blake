class Config:
	# Flask
	SECRET_KEY = "Meow"

	# Flask-SQLAlchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Flask-JWT-Extended
	JWT_SECRET_KEY = "Mew"
	JWT_TOKEN_LOCATION = [ "headers", "cookies"]
	JWT_ACCESS_COOKIE_PATH = "/"
	JWT_REFRESH_COOKIE_PATH = "/token/refresh"
	JWT_COOKIE_CSRF_PROTECT = True
	JWT_CSRF_IN_COOKIES = False

	# Celery
	CELERYD_CONCURRENCY = 2
	CELERYBEAT_SCHEDULER = "app.celery:DatabaseScheduler"


class ProdConfig(Config):
	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blake"

	# Celery
	BROKER_URL = "redis://localhost:6379/0"
	CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

	# Flask-JWT-Extended
	JWT_COOKIE_SECURE = True


class StageConfig(Config):
	# Flask
	DEBUG = True

	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blake-stage"

	# Celery
	BROKER_URL = "redis://localhost:6379/1"
	CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

	# Flask-JWT-Extended
	JWT_COOKIE_SECURE = False


config = {
	"prod": ProdConfig,
	"stage": StageConfig,
	"default": StageConfig
}
