import scrapy

from sebonscraper.items import FpoPipelineItem, FpoApprovedItem


class FpoPipelineSpider(scrapy.Spider):
    name = "sebon_fpo_pipeline"
    start_urls = ["https://www.sebon.gov.np/fpo-pipeline"]
    page_number = 1

    def parse(self, response):
        item = FpoPipelineItem()
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
            FpoPipelineSpider.start_urls[0]
            + "?page="
            + str(FpoPipelineSpider.page_number)
        )

        if FpoPipelineSpider.page_number <= max_page:
            FpoPipelineSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class FpoApprovedSpider(scrapy.Spider):
    name = "sebon_fpo_approved"
    start_urls = ["https://www.sebon.gov.np/fpo-approved"]
    page_number = 1

    def parse(self, response):
        # data = []
        item = FpoApprovedItem()
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
            FpoApprovedSpider.start_urls[0]
            + "?page="
            + str(FpoApprovedSpider.page_number)
        )

        if FpoApprovedSpider.page_number <= max_page:
            FpoApprovedSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)