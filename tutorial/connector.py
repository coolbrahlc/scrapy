from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from .models import QuoteDB,  create_table
from .connector_metaclass import Singleton
import MySQLdb
import logging


DeclarativeBase = declarative_base()
logger = logging.getLogger(__name__)


class DbConnect(metaclass=Singleton):

    def __init__(self):

        self.engine = create_engine(get_project_settings().get("CONNECTION_STRING"))
        self.Session = sessionmaker(bind=self.engine)

    def db_insert(self, item):

        session = self.Session()
        bookdb = QuoteDB(**item)
        bookdb.images = item["images"][0]["path"]
        book_in_db = session.query(QuoteDB).filter_by(book_url=bookdb.book_url).first()

        if book_in_db is None:
            try:
                session.add(bookdb)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

        else:
             logger.info("<-------------------------------------------->")
             logger.info(book_in_db.title)
             logger.info("<---------ALREADY IN ------------------------->")

        return item

    def raw_connect(self, item):

        conn = MySQLdb.connect('localhost', 'root', '',
                               'testbase', charset="utf8",
                               use_unicode=True)
        cursor = conn.cursor()

        try:

            cursor.execute("""
            INSERT INTO books_table (title, book_url, price, rating, available, currency, genre, description,
             product_code, product_type, price_tax, price_no_tax, tax, reviews_count, book_created, image_urls, images)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (
                            item['title'],
                            item['book_url'],
                            item['price'],
                            item['rating'],
                            item['available'],
                            item['currency'],
                            item['genre'],
                            item['description'],
                            item['product_code'],
                            item['product_type'],
                            item['price_tax'],
                            item['price_no_tax'],
                            item['tax'],
                            item['reviews_count'],
                            item['book_created'],
                            item['image_urls'],
                            item["images"][0]["path"]
                           ))
            conn.commit()

        except MySQLdb.Error as e:
            logger.error(e.args)
            # print(e.arg)
        return item
