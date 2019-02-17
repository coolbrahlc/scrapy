from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose, Identity


class BookItemLoader(ItemLoader):
    default_output_processor = Compose(lambda v: v[0])
    image_urls_out = Identity()
