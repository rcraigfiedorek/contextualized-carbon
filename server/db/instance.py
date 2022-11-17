# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/cloud-sql/postgres/sqlalchemy/connect_connector.py

import os

import pg8000
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes

instance_connection_name = os.environ['INSTANCE_CONNECTION_NAME']  # e.g. 'project:region:instance'
db_user = os.environ['DB_USER']  # e.g. 'my-db-user'
db_pass = os.environ['DB_PASS']  # e.g. 'my-db-password'
db_name = os.environ['DB_NAME']
ip_type = IPTypes.PRIVATE if os.environ.get('PRIVATE_IP') else IPTypes.PUBLIC

connector = Connector()


def getconn() -> pg8000.dbapi.Connection:
    return connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=ip_type
    )


db = SQLAlchemy(engine_options=dict(
    creator=getconn,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
))
