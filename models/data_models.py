from sqlalchemy import Column, DateTime, String, Integer, UUID, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

Base = declarative_base()


class Source(Base):
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


class Story(Base):
    __tablename__ = "stories"
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    createdDate = Column(DateTime, unique=False, server_default=text("NOW()"))
    sourceId = Column(UUID, unique=False)
    title = Column(String, unique=False)
    summary = Column(Text, unique=False)
    sourceUri = Column(String, unique=False)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    createdDate = Column(DateTime, unique=False, server_default=text("NOW()"))
    sourceId = Column(UUID, unique=False)
    summary = Column(Text, unique=False, nullable=False)
