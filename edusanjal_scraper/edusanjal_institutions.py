import csv

import requests
from bs4 import BeautifulSoup

baseURL = "https://edusanjal.com"
collegeUrl = "https://edusanjal.com/college/"
schoolUrl = "https://edusanjal.com/school/"


def get_parsed_data(url: str) -> BeautifulSoup:
    """Get bs4 object containing parsed html of given url"""

    source = requests.get(url).text

    return BeautifulSoup(source, "lxml")


def scrape_page_for_institution(link: str) -> list:
    """Scrape page from link to get institution information"""

    print(f"Scraping {link}...")

    soup = get_parsed_data(link)
    institution_divs = soup.find_all(
        "div", attrs={"class": "overflow-hidden bg-white rounded shadow-xl"}
    )

    institutions = []

    for div in institution_divs:
        a_tags = div.find_all("a")
        li_tags = div.find_all("li")

        url = baseURL + a_tags[0]["href"]
        name = a_tags[1].text.strip()
        location = li_tags[-1].text.strip() or None

        accredition = ""
        accreditionLink = ""

        if len(li_tags) > 1:
            accredition = a_tags[2].text.strip()
            accreditionLink = baseURL + a_tags[2]["href"]

        institutions.append(
            dict(
                url=url,
                name=name,
                accredition=accredition,
                accreditionLink=accreditionLink,
                location=location,
            )
        )

    return institutions


def get_page_links(base_url: str, soup: BeautifulSoup) -> list:
    """Get links for college list"""

    total_pages = int(
        soup.find("nav", attrs={"aria-label": "pagination"}).find_all("a")[-2].text
    )

    return [f"{base_url}?page={i}" for i in range(1, total_pages + 1)]


def scrape(base_url: str) -> list:
    """Scrape the institution information"""

    base_page = get_parsed_data(base_url)
    links = get_page_links(base_url, base_page)

    results = []

    for link in links:
        results += scrape_page_for_institution(link)

    return results


def list_to_csv(list_items: list, institution_type: str):
    """Write the list to csv"""

    if len(list_items) != 0:
        field_names = list(list_items[0].keys())
        with open(f"{institution_type}_list.csv", "w") as f:
            csvwriter = csv.DictWriter(f, field_names, delimiter=",")
            csvwriter.writeheader()
            csvwriter.writerows(list_items)


if __name__ == "__main__":

    # result = scrape(collegeUrl)
    # list_to_csv(result, "college")
    result = scrape(schoolUrl)
    list_to_csv(result, "school")
