# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/cloud-sql/postgres/sqlalchemy/connect_connector.py

import os

import pg8000
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes

instance_connection_name = os.environ['INSTANCE_CONNECTION_NAME']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
ip_type = IPTypes.PRIVATE if os.environ.get('PRIVATE_IP') else IPTypes.PUBLIC


def getconn() -> pg8000.dbapi.Connection:
    with Connector() as connector:
        return connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            enable_iam_auth=True,
            ip_type=ip_type
        )


db = SQLAlchemy(engine_options=dict(
    creator=getconn,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
))
