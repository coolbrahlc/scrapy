from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, Float, Boolean, Text, LargeBinary, Numeric, DateTime)
import logging
import datetime
from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class QuoteDB(DeclarativeBase):
    __tablename__ = "books_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_url = Column('book_url', String(255), unique=True)
    book_created = Column('book_created', String(255), nullable=True)
    image_urls = Column('image_urls', String(255), nullable=True)
    images = Column('images', String(255), nullable=True)
    title = Column('title', Text(), nullable=True)
    rating = Column('rating', Integer(), nullable=True)
    price = Column('price', Numeric(8, 2), nullable=True)

    currency = Column('currency', String(20), nullable=True)
    available = Column('available', Integer(), nullable=True)
    genre = Column('genre', String(100), nullable=True)
    description = Column('description', Text(), nullable=True)
    product_code = Column('product_code', String(255), nullable=True)
    product_type = Column('product_type', String(100), nullable=True)
    price_tax = Column('price_tax', Numeric(8, 2), nullable=True)
    price_no_tax = Column('price_no_tax', Numeric(8, 2), nullable=True)
    tax = Column('tax', Numeric(8, 2), nullable=True)
    reviews_count = Column('reviews_count', Integer(), nullable=True)
    created_date = Column('created_at', default=datetime.datetime.now)
    updated_at = Column('updated_at', default=datetime.datetime.now)



