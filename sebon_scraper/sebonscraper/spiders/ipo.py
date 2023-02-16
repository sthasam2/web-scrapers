import scrapy

from sebonscraper.items import IpoPipelineItem, IpoApprovedItem


class IpoPipelineSpider(scrapy.Spider):
    name = "sebon_ipo_pipeline"
    start_urls = ["https://www.sebon.gov.np/ipo-pipeline"]
    page_number = 1

    def parse(self, response):
        # data = []
        item = IpoPipelineItem()
        rawdata = response.css("table.table tbody tr")
        max_page = (len(response.css("ul.pagination li.page-item ::text")) / 2) - 2

        for index in range(len(rawdata)):
            item["name"] = rawdata[index].xpath("td[1]//text()").extract()[0]
            item["date"] = rawdata[index].xpath("td[2]//text()").extract()[0]
            if len(rawdata[index].xpath("td[3]/a/@href").extract()) != 0:
                item["eng_pdf"] = rawdata[index].xpath("td[3]/a/@href").extract()[0]
            if len(rawdata[index].xpath("td[4]/a/@href").extract()) != 0:
                item["nep_pdf"] = rawdata[index].xpath("td[4]/a/@href").extract()[0]

            yield item

        next_page = (
            IpoPipelineSpider.start_urls[0]
            + "?page="
            + str(IpoPipelineSpider.page_number)
        )

        if IpoPipelineSpider.page_number <= max_page:
            IpoPipelineSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class IpoApprovedSpider(scrapy.Spider):
    name = "sebon_ipo_approved"
    start_urls = ["https://www.sebon.gov.np/ipo-approved"]
    page_number = 1

    def parse(self, response):
        item = IpoApprovedItem()
        rawdata = response.css("table.table tbody tr")
        max_page = (len(response.css("ul.pagination li.page-item ::text")) / 2) - 2

        for index in range(len(rawdata)):
            item["name"] = rawdata[index].xpath("td[1]//text()").extract()[0]
            item["date"] = rawdata[index].xpath("td[2]//text()").extract()[0]
            if len(rawdata[index].xpath("td[3]/a/@href").extract()) != 0:
                item["eng_pdf"] = rawdata[index].xpath("td[3]/a/@href").extract()[0]
            if len(rawdata[index].xpath("td[4]/a/@href").extract()) != 0:
                item["nep_pdf"] = rawdata[index].xpath("td[4]/a/@href").extract()[0]

            yield item

        next_page = (
            IpoApprovedSpider.start_urls[0]
            + "?page="
            + str(IpoApprovedSpider.page_number)
        )

        if IpoApprovedSpider.page_number <= max_page:
            IpoApprovedSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)