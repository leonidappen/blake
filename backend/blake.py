import os

from app.application import create_app


app = create_app(os.getenv("FLASK_CONFIG") or "default")
