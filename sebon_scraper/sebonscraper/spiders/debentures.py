import scrapy

from sebonscraper.items import DebenturePipelineItem, DebentureApprovedItem


class DebenturePipelineSpider(scrapy.Spider):
    name = "sebon_debenture_pipeline"
    start_urls = ["https://www.sebon.gov.np/debenture-pipeline"]
    page_number = 1

    def parse(self, response):
        item = DebenturePipelineItem()
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
            DebenturePipelineSpider.start_urls[0]
            + "?page="
            + str(DebenturePipelineSpider.page_number)
        )

        if DebenturePipelineSpider.page_number <= max_page:
            DebenturePipelineSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class DebentureApprovedSpider(scrapy.Spider):
    name = "sebon_debenture_approved"
    start_urls = ["https://www.sebon.gov.np/debenture-approved"]
    page_number = 1

    def parse(self, response):
        # data = []
        item = DebentureApprovedItem()
        rawdata = response.css("table.table tbody tr").extract()
        max_page = (len(response.css("ul.pagination li.page-item ::text")) / 2) - 2

        for index in range(len(rawdata)):

            item["name"] = rawdata[index].partition("<td>")[2].partition("</td>")[0]
            item["date"] = (
                rawdata[index]
                .partition("</td>\n                                            <td>")[2]
                .partition("</td>\n                                            <td><a")[
                    0
                ]
            )
            item["eng_pdf"] = rawdata[index].partition('href="')[2].partition('" t')[0]

            yield item

        next_page = (
            DebentureApprovedSpider.start_urls[0]
            + "?page="
            + str(DebentureApprovedSpider.page_number)
        )

        if DebentureApprovedSpider.page_number <= max_page:
            DebentureApprovedSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)