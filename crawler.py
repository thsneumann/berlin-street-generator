"""
Crawl street directory on https://onlinestreet.de/strassen/in-Freiburg+im+Breisgau.html 
and output info as json
"""

import json
import string
import sys
from bs4 import BeautifulSoup
import requests
import urllib.parse

BASE_URL = "https://onlinestreet.de/strassen/in-Freiburg+im+Breisgau/"

zip_to_district = {
  "79102": "Wiehre",
  "79098": "Altstadt",
  "79112": "Opfingen",
  "79108": "Nord",
  "79104": "Zähringen",
}

streets = []

for letter in string.ascii_uppercase:
    response = requests.get(BASE_URL + letter + ".html")
    soup = BeautifulSoup(response.content, "html.parser")
    streets_table = soup.find("table", class_="table table-striped table-hover")
    if not streets_table:
        continue
    street_links = streets_table.find_all('a')

    for link in street_links:
        response = requests.get(link["href"])
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="table table-condensed")
        tr = table.find_all("tr")
        street = {}
        street_label = table.find("th", string="Straße")
        street["name"] = street_label.next_sibling.string
        zip_label = table.find("th", string="Postleitzahl & Ort")
        zip = zip_label.next_sibling.a.string[:5]
        district_label = table.find("th", string=["Stadtteil", "Stadtteil(e)"])
        if district_label:
            street["districts"] = [district_label.next_sibling.a.string]
        else:
            street["districts"] = [zip_to_district.get(zip, "")]
        street["google_maps_link"] = "https://www.google.de/maps/place/{name},+{zip}+Freiburg+im+Breisgau".format(
          name=urllib.parse.quote_plus(street["name"]),
          zip=zip
        )
        streets.append(street)

        print(street["name"])

with open(sys.argv[1], "w") as file:
    file.write("var STREETS = " + json.dumps(streets) + ";")
