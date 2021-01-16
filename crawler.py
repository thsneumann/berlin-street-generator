"""
Crawl street directory on berlin.kauperts.de 
and output info as json
"""

import json
import string
import sys
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://berlin.kauperts.de/"
STREET_DIR_URL = BASE_URL + "Strassenverzeichnis/"

streets = []

for letter in string.ascii_uppercase:
    response = requests.get(STREET_DIR_URL + letter)
    soup = BeautifulSoup(response.content, "html.parser")
    streets_table = soup.find("table", class_="default streets")
    street_links = streets_table.find_all('a')

    for link in street_links:
        response = requests.get(BASE_URL + link["href"])
        soup = BeautifulSoup(response.content, "html.parser")
        details_table = soup.find("table", id="Detailinformationen")

        street = {}
        street["name"] = link.string
        street["districts"] = []
        for tr in details_table.find_all("tr", class_="district"):
            if not tr.a:
                continue
            street["districts"].append(tr.a.string)
        street["google_maps_link"] = soup.find("a", class_="large button-v5")["href"]
        streets.append(street)

        print(street["name"])

with open(sys.argv[1], "w") as file:
    file.write("var STREETS_OF_BERLIN = " + json.dumps(streets) + ";")
