import os
import traceback

from flask import Flask, request
from werkzeug.exceptions import HTTPException, NotFound, UnsupportedMediaType

# NOTE: this import will likely be replaced by another dependency which will encapsulate routing, validation, etc
from .invoke import invoke


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def route_index():
        return {
            "app": "Rippling Flux Server",
            "version": "dev",
        }

    @app.route("/invoke/{flux_app}", methods=["POST"])
    def route_invoke(flux_app: str):
        return invoke(flux_app, request.get_json())

    @app.errorhandler(404)
    def page_not_found(err: NotFound):
        return err.description, err.code

    @app.errorhandler(415)
    def page_unsupported_media_type(err: UnsupportedMediaType):
        return err.description, err.code

    @app.errorhandler(HTTPException)
    def errorhandler_catch(err: HTTPException):
        return traceback.format_exc(), err.code

    return app
