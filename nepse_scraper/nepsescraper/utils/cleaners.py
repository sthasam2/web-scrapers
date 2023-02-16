import re


def cleanhtml(raw_html):
    cleanr = re.compile(
        "<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|(?:\n|\t|\r|\xa0)"
    )
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def cleanhtml_shorten(raw_html):
    return cleanhtml(raw_html)[:200].strip() + "..."


def clean_merolagani(raw_html):
    cleanr = re.compile(
        "<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|(?:\n|\t|\r)|Close.*css=''>"
    )
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext