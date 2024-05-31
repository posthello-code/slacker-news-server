from alembic import config as alembic_config
from sqlalchemy import (
    MetaData,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

metadata_obj = MetaData()


# init func
def init_postgres():
    POSTGRES_DB_URL = os.getenv("POSTGRES_DB_URL")
    engine = create_engine(POSTGRES_DB_URL)

    alembic_args = [
        "--raiseerr",  # Optional: Raise exceptions for errors
        "upgrade",
        "head",
    ]

    alembic_config.main(argv=alembic_args)

    session = sessionmaker(bind=engine)()
    return session


def close_session(session):
    try:
        session.close()
    except:
        print("already closed")

    exit(0)
