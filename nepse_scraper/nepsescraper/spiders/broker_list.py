import scrapy
import json

from nepsescraper.items import BrokerListItem


class BrokerListSpider(scrapy.Spider):
    name = "broker_list"
    start_urls = ["https://newweb.nepalstock.com/api/nots/member?page=0&size=100"]

    item = BrokerListItem()

    def parse(self, response):
        raw_data = json.loads(response.body)
        brokers = raw_data["content"]

        for broker in brokers:
            yield self.parse_broker_items(broker)

    def parse_broker_items(self, broker: dict):
        """ """

        broker_item = self.item

        broker_item["id"] = broker["id"]
        broker_item["active_status"] = broker["activeStatus"]
        broker_item["member_code"] = broker["memberCode"]
        broker_item["member_name"] = broker["memberName"]
        broker_item["membership_type_master"] = dict(
            id=broker["membershipTypeMaster"]["id"],
            membership_type=broker["membershipTypeMaster"]["membershipType"],
        )
        broker_item["authorized_contact_person"] = broker["authorizedContactPerson"]
        broker_item["authorized_contact_person_number"] = broker[
            "authorizedContactPersonNumber"
        ]
        broker_item["member_tms_link"] = broker["memberTMSLinkMapping"]["tmsLink"]

        member_branches = list()
        for branch in broker["memberBranchMappings"]:
            member_branches.append(
                dict(
                    id=branch["id"],
                    name=branch["branchName"],
                    location=branch["branchLocation"],
                    branch_head=branch["branchHead"],
                    active_status=branch["activeStatus"],
                    phone_number=branch["phoneNumber"],
                    municipality=dict(
                        name=branch["municipality"]["municipalityName"],
                        status=branch["municipality"]["status"],
                    ),
                    district=dict(
                        name=branch["district"]["districtName"],
                        status=branch["district"]["status"],
                    ),
                    province=dict(
                        name=branch["province"]["description"],
                        status=branch["province"]["status"],
                    ),
                )
            )

        broker_item["member_branches"] = member_branches

        return broker_item