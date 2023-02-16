import re


def cleanhtml(raw_html):
    cleanr = re.compile(
        "<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|(?:\n|\t|\r|\xa0)"
    )
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def cleanhtml_shorten(raw_html):
    return cleanhtml(raw_html)[:200].strip() + "..."


def clean_merolagani_shorten(raw_html):
    cleanr = re.compile(
        "<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|(?:\n|\t|\r)|Close.*css=''>"
    )
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext[:200].strip() + "..."


###############
# Date
###############
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


def clean_insurancekhabar_date(raw_str: str) -> str:
    """
    eg. 'प्रकाशित मिति : २९ चैत्र २०७७, आईतवार १४:२८' to '%d %m %YT %H:%M' ie 29 12 2077 14:28
    """
    cleaned = raw_str.replace("प्रकाशित मिति : ", "")
    cleaned = cleaned.partition(", ")[0] + cleaned.partition("ार")[2]
    return unicode_devanagari_to_english_number(
        unicode_month_to_eng_numeral_month(cleaned)
    )
