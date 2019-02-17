import scrapy
import logging
from urllib.parse import urlparse, urljoin
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose, Identity
from ..items import Book
from ..connector import DbConnect
from ..book_loader import BookItemLoader


logger = logging.getLogger(__name__)


class BooksSpider(scrapy.Spider, DbConnect):
    def __init__(self):
        DbConnect.__init__(self)

    name = "books"

    def start_requests(self):

        urls = []
        for i in range(1, 2):
            urls.append(f"http://books.toscrape.com/catalogue/category/books_1/page-{i}.html")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    #def create_session(self):
    #    return self.db_connect()

    def parse(self, response):

        urls = response.css('article.product_pod h3 a::attr(href)').getall()

        for book_url in urls:
            book_url = "http://books.toscrape.com/catalogue/" + book_url.strip("../")
            yield scrapy.Request(book_url, callback=self.parse_book)
        next_page = 'http://books.toscrape.com/catalogue/' + response.css('li.next a::attr(href)').get()

        #if next_page is not None:
        #    yield scrapy.Request(next_page, callback=self.parse, errback=self.errback_httpbin)

    def parse_book(self, response):

        logging.warning(response.status)
        self.logger.info("Visited %s", response.url)

        def star_rating(rating):
            rating_dict = {
                'One': 1,
                'Two': 2,
                'Three': 3,
                'Four': 4,
                'Five': 5
             }
            if rating:
                return rating_dict[rating]

        stars = response.css('.star-rating').xpath("@class").re(r'star-rating (.+)')[0]
        img_url = 'http://books.toscrape.com/' + response.css('div.item img::attr(src)').get().strip("../")
        currency = response.css('p.price_color::text').get()[0]

        book_loader = BookItemLoader(item=Book(), response=response)
        book_loader.add_xpath('book_created', '/html/head/meta[2]/@content')
        book_loader.add_value('book_url',  response.url)
        book_loader.add_value('image_urls', img_url)
        book_loader.add_css('title', 'div.product_main h1::text', TakeFirst())
        book_loader.add_css('price', 'p.price_color::text', re='(\d+\.\d+)')
        book_loader.add_value('currency', currency)
        book_loader.add_value('rating', star_rating(stars))
        book_loader.add_xpath('genre', '//*[@id="default"]/div/div/ul/li[3]/a/text()')
        book_loader.add_xpath('description', '//*[@id="content_inner"]/article/p/text()', TakeFirst())

        table_loader = book_loader.nested_xpath('//*[@id="content_inner"]/article/table')
        table_loader.add_xpath('product_code', 'tr[1]/td/text()')
        table_loader.add_xpath('product_type', 'tr[2]/td/text()')
        table_loader.add_xpath('price_tax', 'tr[3]/td/text()', re='(\d.+)')
        table_loader.add_xpath('price_no_tax', 'tr[4]/td/text()', re='(\d.+)')
        table_loader.add_xpath('tax', 'tr[5]/td/text()', re='(\d.+)')

        book_loader.add_xpath('reviews_count', '//*[@id="content_inner"]/article/table/tr[7]/td/text()')
        book_loader.add_css('available', 'p.instock::text', re='(\d+) available')

        return book_loader.load_item()

    def errback_httpbin(self, failure):

        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)