# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup, SoupStrainer
from html.parser import HTMLParser
import json
FB_URL = "https://www.facebook.com"

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

class FBParser():
    
    def get_fb_post(self, sub_url):
        req = requests.get(FB_URL + sub_url)
        html = BeautifulSoup(
            req.text,
            "html.parser",
            parse_only=SoupStrainer(
                "div",
                attrs={"data-ad-preview": "message"}))

        inner_div = html.find("div", class_="text_exposed_root").find_all("p")
        html_text_data = []
        stripped_data = []
        menu_data = []

        for data in inner_div:
            html_text_data = str(data).replace("<span class=\"text_exposed_hide\">...</span><span class=\"text_exposed_show\"><br/>", "").split("<br/>")
            for text in html_text_data:
                if "€" in strip_tags(text):
                    stripped_data.append(strip_tags(str(text)))
        return stripped_data
