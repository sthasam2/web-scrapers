import scrapy

from sebonscraper.items import MFSPipelineItem, MFSApprovedItem


class MFSPipelineSpider(scrapy.Spider):
    name = "sebon_mfs_pipeline"
    start_urls = ["https://www.sebon.gov.np/mfs-pipeline"]
    page_number = 1

    def parse(self, response):
        item = MFSPipelineItem()
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
            MFSPipelineSpider.start_urls[0]
            + "?page="
            + str(MFSPipelineSpider.page_number)
        )

        if MFSPipelineSpider.page_number <= max_page:
            MFSPipelineSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class MFSApprovedSpider(scrapy.Spider):
    name = "sebon_mfs_approved"
    start_urls = ["https://www.sebon.gov.np/mfs-approved"]
    page_number = 1

    def parse(self, response):
        item = MFSApprovedItem()
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
            MFSApprovedSpider.start_urls[0]
            + "?page="
            + str(MFSApprovedSpider.page_number)
        )

        if MFSApprovedSpider.page_number <= max_page:
            MFSApprovedSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)