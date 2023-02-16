import scrapy
import json

from nepsescraper.items import CompanyDetailItem


class CompanyListSpider(scrapy.Spider):
    name = "company_detail"
    start_urls = ["https://newweb.nepalstock.com/api/nots/company/list/"]

    def parse(self, response):
        raw_data = json.loads(response.body)

        ids = []
        for data in raw_data:
            ids.append(data["id"])

        for id in ids:
            yield response.follow(
                "https://newweb.nepalstock.com/api/nots/security/" + str(id),
                callback=self.parse_detail,
            )
        # yield response.follow(
        #     "https://newweb.nepalstock.com/api/nots/security/" + str(ids[0]),
        #     callback=self.parse_detail,
        # )

    def parse_detail(self, response):
        try:
            raw_data = json.loads(response.body)

            item = CompanyDetailItem()

            # value_or_None = lambda x: None if x is None else x

            # security details
            item["security_symbol"] = raw_data["security"]["symbol"]
            item["security_name"] = raw_data["security"]["securityName"]
            item["isin"] = raw_data["security"]["isin"]
            item["security_id"] = raw_data["securityId"]

            # t_or_f = lambda x : True if x=="Y" or x=="y" else False
            # item["permitted_to_trade"]= t_or_f(raw_data["security"]["permittedToTrade"])

            # Status
            item["permitted_to_trade"] = raw_data["security"]["permittedToTrade"]
            item["company_id_active_status"] = raw_data["security"]["companyId"][
                "activeStatus"
            ]
            item["is_promoter"] = raw_data["security"]["isPromoter"]

            #  Dates # FIXME: fix datetime
            item["updated_date"] = raw_data["updatedDate"]
            item["listing_date"] = raw_data["security"]["listingDate"]
            item["capital_gain_base_date"] = raw_data["security"]["capitalGainBaseDate"]
            item["trading_start_date"] = raw_data["security"]["tradingStartDate"]

            # instrument type
            item["instrument_type_id"] = raw_data["security"]["instrumentType"]["id"]
            item["instrument_type_code"] = raw_data["security"]["instrumentType"][
                "code"
            ]
            item["instrument_type_description"] = raw_data["security"][
                "instrumentType"
            ]["description"]

            #  Share group
            item["share_group_id"] = raw_data["security"]["shareGroupId"]["id"]
            item["share_group_name"] = raw_data["security"]["shareGroupId"]["name"]
            item["share_group_description"] = raw_data["security"]["shareGroupId"][
                "description"
            ]
            item["share_group_capital_range_min"] = raw_data["security"][
                "shareGroupId"
            ]["capitalRangeMin"]

            # Company
            item["company_id"] = raw_data["security"]["companyId"]["id"]
            item["company_email"] = raw_data["security"]["companyId"]["email"]
            item["company_website"] = raw_data["security"]["companyId"][
                "companyWebsite"
            ]
            item["company_contact_person"] = raw_data["security"]["companyId"][
                "companyContactPerson"
            ]
            item["company_active"] = raw_data["security"]["companyId"]["activeStatus"]

            #  Sector
            item["sector_id"] = raw_data["security"]["companyId"]["sectorMaster"]["id"]
            item["sector_description"] = raw_data["security"]["companyId"][
                "sectorMaster"
            ]["sectorDescription"]

            #  Share Data
            item["face_value"] = raw_data["security"]["faceValue"]
            item["net_worth_base_price"] = raw_data["security"][
                "networthBasePrice"
            ]  # REVIEW Baseprice
            item["stock_listed_shares"] = raw_data["stockListedShares"]
            item["paid_up_capital"] = raw_data["paidUpCapital"]
            item["issued_capital"] = raw_data["issuedCapital"]
            item["market_capitalization"] = raw_data["marketCapitalization"]
            item["public_shares"] = raw_data["publicShares"]
            item["public_percentage"] = raw_data["publicPercentage"]
            item["promoter_shares"] = raw_data["promoterShares"]
            item["promoter_percentage"] = raw_data["promoterPercentage"]

            yield item

        except KeyError as e:
            print(e)

    def parse_detail1(self, response):
        """
        Discarded cuz more memory and processor usage
        """

        raw_data = json.loads(response.body)

        item = CompanyDetailItem()

        key_values = {
            "security_symbol": ["security", "symbol"],
            "security_name": ["security", "securityName"],
            "isin": ["security", "isin"],
            "security_id": ["securityId"],
            # Status
            "permitted_to_trade": ["security", "permittedToTrade"],
            "company_id_active_status": ["security", "companyId", "activeStatus"],
            "is_promoter": ["security", "isPromoter"],
            #  Dates
            "updated_date": ["updatedDate"],
            "listing_date": ["security", "listingDate"],
            "capital_gain_base_date": ["security", "capitalGainBaseDate"],
            "trading_start_date": ["security", "tradingStartDate"],
            # instrument type
            "instrument_type_id": ["security", "instrumentType", "id"],
            "instrument_type_code": ["security", "instrumentType", "code"],
            "instrument_type_description": [
                "security",
                "instrumentType",
                "description",
            ],
            #  Share group
            "share_group_id": ["security", "shareGroupId", "id"],
            "share_group_name": ["security", "shareGroupId", "name"],
            "share_group_description": ["security", "shareGroupId", "description"],
            "share_group_capital_range_min": [
                "security",
                "shareGroupId",
                "capitalRangeMin",
            ],
            # Company
            "company_id": ["security", "companyId", "id"],
            "company_email": ["security", "companyId", "email"],
            "company_website": ["security", "companyId", "companyWebsite"],
            "company_contact_person": ["security", "companyId", "companyContactPerson"],
            "company_active": ["security", "companyId", "activeStatus"],
            #  Sector
            "sector_id": ["security", "companyId", "sectorMaster", "id"],
            "sector_description": [
                "security",
                "companyId",
                "sectorMaster",
                "sectorDescription",
            ],
            #  Share Data
            "face_value": ["security", "faceValue"],
            "net_worth_base_price": ["security", "networthBasePrice"],
            "stock_listed_shares": ["stockListedShares"],
            "paid_up_capital": ["paidUpCapital"],
            "issued_capital": ["issuedCapital"],
            "market_capitalization": ["marketCapitalization"],
            "public_shares": ["publicShares"],
            "public_percentage": ["publicPercentage"],
            "promoter_shares": ["promoterShares"],
            "promoter_percentage": ["promoterPercentage"],
        }
        # FIXME refactor code to use loop

        for key, values in key_values.items():
            temp = raw_data

            for value in values:
                if not temp[value]:
                    temp = None
                else:
                    temp = temp[value]

            item[key] = temp
