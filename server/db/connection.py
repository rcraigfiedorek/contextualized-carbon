from flask_sqlalchemy import SQLAlchemy

from db.secrets import get_db_password

DB_DRIVER = 'postgresql+pg8000'
DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'corporate-emissions'
DB_USER = 'postgres'
DB_PASSWORD = get_db_password()
DB_URL = f'{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db = SQLAlchemy(engine_options=dict(
    url=DB_URL,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
))
