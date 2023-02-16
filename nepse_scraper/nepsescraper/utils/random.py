import humps


def print_snake(dict):
    a = []
    b = []
    for key, value in dict.items():
        a.append(humps.decamelize(key))
        b.append(key)
        print(humps.decamelize(key), "= scrapy.Field()")
    return [a, b]


def print_scrapy_item_names(list):
    for doc in list:
        print(f'item["{doc.partition(" = ")[0]}"]=')


a = (
    [
        "security_symbol = scrapy.Field()",
        "security_name = scrapy.Field()",
        "isin = scrapy.Field()",
        "permitted_to_trade = scrapy.Field()",
        "listing_date = scrapy.Field()",
        "instrument_type_id = scrapy.Field()",
        "instrument_type_code = scrapy.Field()",
        "instrument_type_description = scrapy.Field()",
        "capital_gain_base_date = scrapy.Field()",
        "face_value = scrapy.Field()",
        "net_worth_base_price = scrapy.Field()",
        "share_group_id = scrapy.Field()",
        "share_group_name = scrapy.Field()",
        "share_group_description = scrapy.Field()",
        "share_group_capital_range_min = scrapy.Field()",
        "active_status = scrapy.Field()",
        "trading_start_date = scrapy.Field()",
        "is_promoter = scrapy.Field()",
        "company_id = scrapy.Field()",
        "company_email = scrapy.Field()",
        "company_website = scrapy.Field()",
        "company_contact_person = scrapy.Field()",
        "company_active = scrapy.Field()",
        "sector_id = scrapy.Field()",
        "sector_description = scrapy.Field()",
        "stock_listed_shares = scrapy.Field()",
        "paid_up_capital = scrapy.Field()",
        "issued_capital = scrapy.Field()",
        "market_capitalization = scrapy.Field()",
        "public_shares = scrapy.Field()",
        "public_percentage = scrapy.Field()",
        "promoter_shares = scrapy.Field()",
        "promoter_percentage = scrapy.Field()",
        "updated_date = scrapy.Field()",
        "security_id = scrapy.Field()",
    ],
)


"""
item["security_symbol"]=
item["security_name"]=
item["isin"]=
item["permitted_to_trade"]=
item["listing_date"]=
item["instrument_type_id"]=
item["instrument_type_code"]=
item["instrument_type_description"]=
item["capital_gain_base_date"]=
item["face_value"]=
item["net_worth_base_price"]=
item["share_group_id"]=
item["share_group_name"]=
item["share_group_description"]=
item["share_group_capital_range_min"]=
item["active_status"]=
item["trading_start_date"]=
item["is_promoter"]=
item["company_id"]=
item["company_email"]=
item["company_website"]=
item["company_contact_person"]=
item["company_active"]=
item["sector_id"]=
item["sector_description"]=
item["stock_listed_shares"]=
item["paid_up_capital"]=
item["issued_capital"]=
item["market_capitalization"]=
item["public_shares"]=
item["public_percentage"]=
item["promoter_shares"]=
item["promoter_percentage"]=
item["updated_date"]=
item["security_id"]="""

{
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
    "instrument_type_description": ["security", "instrumentType", "description"],
    #  Share group
    "share_group_id": ["security", "shareGroupId", "id"],
    "share_group_name": ["security", "shareGroupId", "name"],
    "share_group_description": ["security", "shareGroupId", "description"],
    "share_group_capital_range_min": ["security", "shareGroupId", "capitalRangeMin"],
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

{
    "securityId": "2809",
    "openPrice": 1365,
    "highPrice": 1415,
    "lowPrice": 1338,
    "totalTradeQuantity": 48189,
    "totalTrades": 443,
    "lastTradedPrice": 1364,
    "previousClose": 1390,
    "businessDate": "2021-04-26",
    "closePrice": None,
    "fiftyTwoWeekHigh": 1720,
    "fiftyTwoWeekLow": 414,
    "lastUpdatedDateTime": "2021-04-26T14:48:42.016058",
}