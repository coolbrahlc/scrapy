# -*- coding: utf-8 -*-
import json
import logging
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Table, ForeignKey
from .models import QuoteDB
from .connector import DbConnect
logger = logging.getLogger(__name__)
DeclarativeBase = declarative_base()


class BooksPipeline:

    def open_spider(self, spider):
        #self.file = open('items555.jl', 'w')
        pass

    def close_spider(self, spider):
        #self.file.close()
        pass

    def process_item(self, item, spider):

        return spider.db_insert(item)
        #return spider.raw_connect(item)











        '''
        session = spider.create_session()
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
        '''

    def process_item2(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

