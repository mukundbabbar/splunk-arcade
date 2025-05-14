from concurrent.futures import ThreadPoolExecutor
from flask import Flask

from src.routes import routes
from src.dummy_scores import generate


def create_app():
    app = Flask(__name__)

    app.register_blueprint(routes)

    return app


def run_dummy_scores():
    ThreadPoolExecutor(max_workers=1).submit(generate)
