from alembic import config as alembic_config
from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    create_engine,
    inspect,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

load_dotenv()

metadata_obj = MetaData()

# Database classes
Base = declarative_base()


class sources(Base):
    __tablename__ = "sources"
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    source = Column(String, unique=False)
    createdDate = Column(DateTime, unique=False, server_default=text("NOW()"))
    sourceMethod = Column(String, unique=False)
    sourceUri = Column(String, unique=False)
    dataFormat = Column(String, unique=False)
    content = Column(Text, unique=False)
    externalId = Column(Integer, unique=False)


class stories(Base):
    __tablename__ = "stories"
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    createdDate = Column(DateTime, unique=False, server_default=text("NOW()"))
    sourceId = Column(UUID, unique=False)
    title = Column(String, unique=False)
    summary = Column(Text, unique=False)
    sourceUri = Column(String, unique=False)


# init func
def init_postgres():
    POSTGRES_DB_URL = os.getenv("POSTGRES_DB_URL")
    engine = create_engine(POSTGRES_DB_URL)

    def table_exists(engine, table_name):
        ins = inspect(engine)
        return ins.dialect.has_table(engine.connect(), table_name)

    # Print the names of all tables in the database
    def print_all_tables(engine):
        metadata = MetaData()
        metadata.reflect(bind=engine)
        tables = metadata.tables.keys()
        print("List of tables:")
        for table in tables:
            print(table)

    if not table_exists(engine, "stories") or not table_exists(engine, "sources"):
        print("Initializing table")
        Base.metadata.create_all(engine)
        print_all_tables(engine)

    alembic_args = [
        "--raiseerr",  # Optional: Raise exceptions for errors
        "upgrade",
        "head",
    ]

    alembic_config.main(argv=alembic_args)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session
