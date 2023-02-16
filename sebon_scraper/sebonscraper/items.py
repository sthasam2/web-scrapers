import scrapy
from scrapy.item import Field


class SebonscraperItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    eng_pdf = scrapy.Field()


class IpoPipelineItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    eng_pdf = scrapy.Field()


class IpoApprovedItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    eng_pdf = scrapy.Field()


class DebenturePipelineItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    eng_pdf = scrapy.Field()


class DebetureApprovedItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    eng_pdf = scrapy.Field()


class MFSPipelineItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    eng_pdf = scrapy.Field()


class MFSApprovedItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    eng_pdf = scrapy.Field()


class PublicIssuesItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    eng_pdf = scrapy.Field()