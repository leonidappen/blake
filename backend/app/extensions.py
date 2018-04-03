
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery

from app.models.base import base

db = SQLAlchemy(model_class=base)
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
celery = Celery()
