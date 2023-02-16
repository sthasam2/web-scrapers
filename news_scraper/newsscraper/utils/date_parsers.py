import datetime as dt

import nepali_datetime as ndt
import pytz


# class DateParser:
def oldnepalstock_to_default(oldnepse_date: str) -> str:
    """
    Returns 'As of yyyy-mm-dd HH:MM:SS' by parsing into 'dd month, yyyy HH:MMam/pm' format
    """
    return dt.datetime.strptime(oldnepse_date, "As of %Y-%m-%d %H:%M:%S").strftime(
        "%d %B, %Y %I:%M%p"
    )


def t_to_default(t_date: str) -> str:
    """
    Returns 'yyyy-mm-ddTHH:MM:SS' by parsing into 'dd month, yyyy HH:MMam/pm' format
    """
    dt_naive = dt.datetime.strptime(t_date, "%Y-%m-%dT%H:%M:%S")
    timezone = pytz.timezone("Asia/Kathmandu")
    dt_aware = timezone.localize(dt_naive)
    return dt_aware.strftime("%d %B, %Y %I:%M%p")


def t_to_nep_default(t_date: str) -> str:
    """
    Returns 'yyyy-mm-ddTHH:MM:SS' by parsing into Nepali 'dd month, yyyy HH:MMam/pm' format
    """
    return ndt.datetime.strptime(t_date, "%Y-%m-%dT%H:%M:%S").strftime(
        "%d %B, %Y %I:%M%p"
    )


######################
# Unicode Conversions
######################


def unicode_devanagari_to_english_number(dev_str: str) -> str:
    """
    Converts devanagari numbers into arabic numerals 1,2, ...
    """
    str_dict = {
        "०": "0",
        "१": "1",
        "२": "2",
        "३": "3",
        "४": "4",
        "५": "5",
        "६": "6",
        "७": "7",
        "८": "8",
        "९": "9",
    }
    new_str = dev_str
    for char in new_str:
        char in str_dict
        if char in str_dict:
            new_str = new_str.replace(char, str_dict[char])
    return new_str


def english_number_to_unicode_devanagari(dev_str: str) -> str:
    """
    Converts devanagari numbers into arabic numerals 1,2, ...
    """
    str_dict = {
        "0": "०",
        "1": "१",
        "2": "२",
        "3": "३",
        "4": "४",
        "5": "५",
        "6": "६",
        "7": "७",
        "8": "८",
        "9": "९",
    }
    new_str = dev_str
    for char in new_str:
        char in str_dict
        if char in str_dict:
            new_str = new_str.replace(char, str_dict[char])
    return new_str


def unicode_month_to_eng_numeral_month(dev_str: str) -> int:
    """
    Converts devanagiri bikram sambat months to arabian numeral months integer
    e.g. 'वैशाख' to 01
    """
    str_dict = {
        "वैशाख": "01",
        "जेष्ठ": "02",
        "असार": "03",
        "श्रावण": "04",
        "भदौ": "05",
        "आश्विन": "06",
        "कार्तिक": "07",
        "मंसिर": "08",
        "पौष": "09",
        "माघ": "10",
        "फाल्गुण": "11",
        "चैत्र": "12",
    }
    new_str = dev_str.split(" ")
    for index, word in enumerate(new_str):
        word in str_dict
        if word in str_dict:
            new_str[index] = str_dict[word]
    return " ".join(new_str)


######################
# Datetime conversions
######################


def to_datetime(date: str, date_format: str):
    """
    Converts date string of given format--date_format to datetime
    eg. 2001-02-05 (%Y-%m-%d) to datetime.datetime(2001,02,05,0,0,0,tzname)
    """
    return pytz.timezone("Asia/Kathmandu").localize(
        dt.datetime.strptime(date, date_format)
    )


def to_nep_datetime(date: str, date_format: str):
    """
    Converts unicode converted ie english number only nepali date string
    of given format--date_format to datetime
    eg. 2065-02-05 (%Y-%m-%d) to neplai_datetime.datetime(2065,02,05,0,0,0,tzname)
    """
    cleaned = unicode_devanagari_to_english_number(date)

    return ndt.datetime.strptime(cleaned, date_format)


def from_nep_to_eng_datetime(date: str, date_format: str):
    """
    Converts nepali datetime to english datetime
    """
    cleaned = unicode_devanagari_to_english_number(date)
    print(cleaned)
    nep = ndt.datetime.strptime(cleaned, date_format)
    eng = ndt.datetime.to_datetime_date(nep.date())

    return dt.datetime(
        eng.year,
        eng.month,
        eng.day,
        nep.hour,
        nep.minute,
        nep.second,
        nep.microsecond,
        nep.tzinfo,
    )


def from_eng_to_nep_datetime(date: str, date_format: str):
    """
    Converts english datetime to nepali datetime
    """
    eng = dt.datetime.strptime(date, date_format)
    nep = ndt.datetime.from_datetime_date(eng.date())

    return ndt.datetime(
        nep.year, nep.month, nep.day, eng.hour, eng.minute, eng.second, eng.microsecond
    )


########################################
# Datetime to custom date format strings
########################################
def to_eng_custom(date_time: dt.datetime) -> str:
    """
    Converts datetime to custom format
    eg. 2000-03-14 (%Y-%m-%d) to 14 March 2000, Tuesday
    """
    # print(date_time.time, "///////////////\n")

    if date_time.time() == dt.time(0, 0, 0, 0):
        return date_time.strftime("%d %B %Y, %A")
    else:
        return date_time.strftime("%d %B %Y, %A %I:%M%p")


def to_nep_custom(date_time: ndt.datetime) -> str:
    """
    Converts datetime to custom format
    eg. 2056-12-01 (%Y-%m-%d) to  March 2000, Tuesday
    """
    # print(date_time.time, "///////////////\n")
    if date_time.time() == dt.time(0, 0, 0, 0):
        return english_number_to_unicode_devanagari(date_time.strftime("%d %B %Y, %A"))
    else:
        return english_number_to_unicode_devanagari(
            date_time.strftime("%d %N %K, %G %I:%M%p")
        )


def get_current_datetime_eng_custom():
    """
    Returns current datetime in custom string format
    """
    return to_eng_custom(dt.datetime.now())


def get_custom_dates(str_date: str, date_format: str):
    """
    Gives custom english and nepali dates in custom format
    """
    # convert english
    try:
        eng = to_eng_custom(to_datetime(str_date, date_format))
    except:
        eng = to_eng_custom(from_nep_to_eng_datetime(str_date, date_format))
    # convert nepali
    try:
        nep = to_nep_custom(to_nep_datetime(str_date, date_format))
    except:
        nep = to_nep_custom(from_eng_to_nep_datetime(str_date, date_format))

    return {"eng": eng, "nep": nep}