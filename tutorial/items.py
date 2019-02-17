# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Book(scrapy.Item):

    image_urls = scrapy.Field()
    images = scrapy.Field()

    book_url = scrapy.Field()
    book_created = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    available = scrapy.Field()
    rating = scrapy.Field()
    genre = scrapy.Field()
    description = scrapy.Field()
    product_code = scrapy.Field()
    product_type = scrapy.Field()
    price_tax = scrapy.Field()
    price_no_tax = scrapy.Field()
    tax = scrapy.Field()
    reviews_count = scrapy.Field()
    currency = scrapy.Field()

