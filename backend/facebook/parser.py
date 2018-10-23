# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup, SoupStrainer
from html.parser import HTMLParser
import re
import json

FB_URL = "https://www.facebook.com"

# regex matches : 14.00, 14,00, 14.- and even 1.170
PRICE_PATTERN = '(\d{1,2}(\.|\,)\d+)|(\d{1,2}.-)'


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def rahvatoit_condition(text):
    accepted_strings = ["TTÜ", "Raamatukogu", "Soc"]
    for item in accepted_strings:
        if (item.lower() in text.lower()):
            return True


def menu_item_condition(text):
    regex = re.compile(PRICE_PATTERN)
    if (("€" in text or regex.search(text)) and "menüü" not in text):
        return True


def price_matches_multiple_condition(text):
    if len(re.findall(PRICE_PATTERN, text)) > 1:
        return True


def split_on_multiple_price_matches(text):
    match = re.search(PRICE_PATTERN, text)
    return text[:match.end()], text[match.end():]


class FBParser():

    def get_fb_post(self, sub_url, numberOfPosts=1):
        req = requests.get(FB_URL + sub_url)
        html = BeautifulSoup(
            req.text,
            "html.parser",
            parse_only=SoupStrainer(
                "div",
                attrs={"data-ad-preview": "message"}))
        
        inner_div = html.find_all("div", class_="text_exposed_root")
        html_text_data = []
        stripped_data = []
        menu_data = []
        for postNr in range(len(inner_div)):
            if postNr > numberOfPosts:
                break
            else:
                for data in inner_div[postNr]:
                    html_text_data = str(data).replace("<span class=\"text_exposed_hide\">...</span><span class=\"text_exposed_show\"><br/>", "").split("<br/>")
                    for text in html_text_data:
                        stripped_string = strip_tags(text)
                        if rahvatoit_condition(stripped_string):
                            stripped_data.append(stripped_string)

                        if menu_item_condition(stripped_string):
                            # if more than one price on line, split them and append separately
                            if price_matches_multiple_condition(stripped_string):
                                split_strings = split_on_multiple_price_matches(stripped_string)
                                for item in split_strings:
                                    stripped_data.append(item)
                            else:
                                stripped_data.append(stripped_string)

        return stripped_data

