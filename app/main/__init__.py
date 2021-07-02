from flask import Flask
from flask_restful import Api
from flask_caching import Cache

from .controller.status import APIStatus
from .config import (
    config_by_name,
    API_PREFIX,
    CACHE_CONFIG
)

cache = Cache()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    cache.init_app(app, config=CACHE_CONFIG)

    return app


def load_routes(app):
    from .controller.blog_posts import (
        PostsList
    )
    api = Api(app)
    api.add_resource(APIStatus, f"{API_PREFIX}/ping", endpoint="api-status")
    api.add_resource(PostsList, f"{API_PREFIX}/posts", endpoint="posts")

    return api
