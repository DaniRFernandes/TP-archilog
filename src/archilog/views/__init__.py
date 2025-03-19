from flask import Flask

from archilog.views.cli import cli


def create_app():
    from archilog.views.web import web_ui

    app = Flask(__name__)
    app.register_blueprint(web_ui)
    app.config.from_prefixed_env(prefix="ARCHILOG_FLASK")

    return app
