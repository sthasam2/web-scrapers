import scrapy

from sebonscraper.items import PublicIssuesPipelineItem, PublicIssuesApprovedItem


class PublicIssuesPipelineSpider(scrapy.Spider):
    name = "sebon_public_issues_data"
    start_urls = ["https://www.sebon.gov.np/public-issues-data"]
    page_number = 1

    def parse(self, response):
        item = PublicIssuesPipelineItem()
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
            PublicIssuesPipelineSpider.start_urls[0]
            + "?page="
            + str(PublicIssuesPipelineSpider.page_number)
        )

        if PublicIssuesPipelineSpider.page_number <= max_page:
            PublicIssuesPipelineSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
