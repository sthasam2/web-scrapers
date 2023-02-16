# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MarketSummaryItem(scrapy.Item):
    updated_date = scrapy.Field()
    total_turnover = scrapy.Field()
    total_traded_shares = scrapy.Field()
    total_transactions = scrapy.Field()
    total_scrips_traded = scrapy.Field()
    total_market_cap = scrapy.Field()
    floated_market_cap = scrapy.Field()
