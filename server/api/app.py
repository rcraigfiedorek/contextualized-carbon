from apiflask import APIFlask
from flask.cli import AppGroup

from api.api import bp
from db import db, envirofacts_pipeline

app = APIFlask(__name__, openapi_blueprint_url_prefix='/api')
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='postgresql+pg8000://',
)
db.init_app(app)

AppGroup('db').command('init')(envirofacts_pipeline)

app.register_blueprint(bp)