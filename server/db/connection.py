import pg8000
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes

from db.secrets import get_secret_value

PROJECT_ID = 'delta-timer-368701'
DB_ZONE = 'us-central1'
DB_NAME = 'corporate-emissions'
DB_USER = 'postgres'
DB_CONNECTION_NAME = f'{PROJECT_ID}:{DB_ZONE}:{DB_NAME}'
DB_PASSWORD = get_secret_value('EMISSIONS_DB_PASSWORD')


def getconn() -> pg8000.dbapi.Connection:
    with Connector() as connector:
        return connector.connect(
            DB_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            enable_iam_auth=True,
            ip_type=IPTypes.PUBLIC
        )


db = SQLAlchemy(engine_options=dict(
    creator=getconn,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
))
