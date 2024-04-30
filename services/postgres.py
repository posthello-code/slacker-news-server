from sqlalchemy import JSON, UUID, Column, DateTime, MetaData, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
load_dotenv()

metadata_obj = MetaData()

# Database classes
Base = declarative_base()
class stories(Base):
    __tablename__ = 'stories'
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    story = Column(JSON, unique=False)
    date = Column(DateTime, unique=False, server_default=text('NOW()'))


# init func
def init_postgres():
    # DB Setup
    POSTGRES_DB_URL = os.getenv("POSTGRES_DB_URL")
    engine = create_engine(POSTGRES_DB_URL)
    table_name = 'stories'

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

    if not table_exists(engine, table_name):
        print("Initializing table")
        Base.metadata.create_all(engine)
        print_all_tables(engine)
        
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
        