import scrapy


class NewsItem(scrapy.Item):
    # source
    source = scrapy.Field()
    # titles
    headline = scrapy.Field()
    subtitle = scrapy.Field()
    # dates
    date = scrapy.Field()
    nepdate = scrapy.Field()
    scraped_datetime = scrapy.Field()
    # urls
    image_url = scrapy.Field()
    url = scrapy.Field()
    # scrips
    scrip = scrapy.Field()
