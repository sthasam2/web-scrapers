# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiveMarketItem(scrapy.Item):
    security_id = scrapy.Field()
    symbol = scrapy.Field()
    company = scrapy.Field()
    ltp = scrapy.Field()
    ltv = scrapy.Field()
    point_change = scrapy.Field()
    perc_change = scrapy.Field()
    open_price = scrapy.Field()
    high_price = scrapy.Field()
    low_price = scrapy.Field()
    volume = scrapy.Field()
    prev_closing = scrapy.Field()


class FloorsheetItem(scrapy.Item):
    contract_id = scrapy.Field()
    stock_symbol = scrapy.Field()
    buyer_member_id = scrapy.Field()
    seller_member_id = scrapy.Field()
    contract_quantity = scrapy.Field()
    contract_rate = scrapy.Field()
    contract_amount = scrapy.Field()
    business_date = scrapy.Field()
    trade_book_id = scrapy.Field()
    stock_id = scrapy.Field()
    buyer_broker_name = scrapy.Field()
    seller_broker_name = scrapy.Field()
    security_name = scrapy.Field()


class MarketSummaryItem(scrapy.Item):
    updated_date = scrapy.Field()
    total_turnover = scrapy.Field()
    total_traded_shares = scrapy.Field()
    total_transactions = scrapy.Field()
    total_scrips_traded = scrapy.Field()
    total_market_cap = scrapy.Field()
    floated_market_cap = scrapy.Field()


class CompanyListItem(scrapy.Item):
    id = scrapy.Field()
    company_name = scrapy.Field()
    symbol = scrapy.Field()
    security_name = scrapy.Field()
    status = scrapy.Field()
    company_email = scrapy.Field()
    website = scrapy.Field()
    sector_name = scrapy.Field()
    regulatory_body = scrapy.Field()
    instrument_type = scrapy.Field()


class CompanyDetailItem(scrapy.Item):
    # security details
    security_symbol = scrapy.Field()
    security_name = scrapy.Field()
    isin = scrapy.Field()
    security_id = scrapy.Field()

    # Status
    permitted_to_trade = scrapy.Field()
    company_id_active_status = scrapy.Field()
    is_promoter = scrapy.Field()

    #  Dates
    updated_date = scrapy.Field()
    listing_date = scrapy.Field()
    capital_gain_base_date = scrapy.Field()
    trading_start_date = scrapy.Field()

    # instrument type
    instrument_type_id = scrapy.Field()
    instrument_type_code = scrapy.Field()
    instrument_type_description = scrapy.Field()

    #  Share group
    share_group_id = scrapy.Field()
    share_group_name = scrapy.Field()
    share_group_description = scrapy.Field()

    share_group_capital_range_min = scrapy.Field()

    # Company
    company_id = scrapy.Field()
    company_email = scrapy.Field()
    company_website = scrapy.Field()
    company_contact_person = scrapy.Field()

    company_active = scrapy.Field()

    #  Sector
    sector_id = scrapy.Field()
    sector_description = scrapy.Field()

    #  Share Data
    face_value = scrapy.Field()
    net_worth_base_price = scrapy.Field()
    stock_listed_shares = scrapy.Field()
    paid_up_capital = scrapy.Field()
    issued_capital = scrapy.Field()
    market_capitalization = scrapy.Field()
    public_shares = scrapy.Field()
    public_percentage = scrapy.Field()
    promoter_shares = scrapy.Field()
    promoter_percentage = scrapy.Field()


class CompanyTradeDetailItem(scrapy.Item):
    """"""

    security_symbol = scrapy.Field()
    security_name = scrapy.Field()
    security_id = scrapy.Field()
    open_price = scrapy.Field()
    high_price = scrapy.Field()
    low_price = scrapy.Field()
    total_trade_quantity = scrapy.Field()
    total_trades = scrapy.Field()
    last_traded_price = scrapy.Field()
    previous_close = scrapy.Field()
    business_date = scrapy.Field()
    close_price = scrapy.Field()
    fifty_two_week_high = scrapy.Field()
    fifty_two_week_low = scrapy.Field()
    last_updated_date_time = scrapy.Field()


class CompanyPriceDetailItem(scrapy.Item):
    """"""

    id = scrapy.Field()
    business_date = scrapy.Field()
    last_updated_time = scrapy.Field()

    security_symbol = scrapy.Field()
    security_name = scrapy.Field()
    security_id = scrapy.Field()

    open_price = scrapy.Field()
    high_price = scrapy.Field()
    low_price = scrapy.Field()
    close_price = scrapy.Field()

    total_traded_quantity = scrapy.Field()
    total_traded_value = scrapy.Field()
    total_trades = scrapy.Field()
    last_traded_price = scrapy.Field()
    average_traded_price = scrapy.Field()
    previous_day_close_price = scrapy.Field()

    fifty_two_week_high = scrapy.Field()
    fifty_two_week_low = scrapy.Field()


class BrokerListItem(scrapy.Item):
    """ """

    id = scrapy.Field()
    active_status = scrapy.Field()
    member_code = scrapy.Field()
    member_name = scrapy.Field()
    membership_type_master = scrapy.Field()
    authorized_contact_person = scrapy.Field()
    authorized_contact_person_number = scrapy.Field()
    member_tms_link = scrapy.Field()
    member_branches = scrapy.Field()

    pass
