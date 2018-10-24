import requests
from bs4 import BeautifulSoup, SoupStrainer
import backend.util as util
import re

PDF_URL = "http://www.daily.ee/files/dn_daily_nadalamenuu_ttu_6_korpus.pdf"
PDF_PATH = './data/vimenu.pdf'
TXT_PATH = './data/vimenu.txt'
BEFORE_PRICE_PATTERN = '(?:(?!\d+\.\d+).)*'
PRICE_PATTERN = '(\d{1,2}(\.|\,)\d+)|(\d{1,2}.-)'

class DailyParser():
    dates = []

    def get_daily_menu(self, url):
        req = requests.get(url)
        html = BeautifulSoup(
            req.text,
            "html.parser",
            parse_only=SoupStrainer(
                "div",
                class_="left"))
        divs = html.find_all("div", class_="offer")
        stripped_data = []
        for div in divs:
            stripped_data.append(util.strip_tags(str(div)))

        return stripped_data

    def get_pdfalt_menu(self, url):
        if not util.up_to_date_file_exists(TXT_PATH):
            util.download_pdf(PDF_URL, PDF_PATH)
            if util.wait_until_file_exists(PDF_PATH):
                proc = util.get_subprocess('pdftotext', ['-raw', PDF_PATH])

        if util.wait_until_file_exists(TXT_PATH):
            output = open('./data/vimenu.txt', 'r').readlines()
            return self.format_menu(output)

    def format_menu(self, menu):
        stripped_list = []
        STATIC_MENU_TEXT = "Praadide hinnad on antud 100 g kohta. Toit kaalutakse kassas."
        for line in menu:
            stripped_list.append(str(line.lstrip().rstrip()))

        # remove name and address line
        del stripped_list[0]

        # remove this line
        if "Lõunarestoran" in stripped_list:
            stripped_list.remove("Lõunarestoran")

        # iterate over list and remove date lines from the middle and add them to separate list
        more_stripped_list = self.remove_dates_from_list(stripped_list)

        # iterate over list and merge english line into estonian and add price
        formatted_list = self.merge_est_eng_lines(more_stripped_list)

        # all menus as lists into a list and return that
        return self.multiple_days_lists(formatted_list, STATIC_MENU_TEXT)

    def remove_dates_from_list(self, stripped_list):
        days = ["Esmaspäev", "Teisipäev", "Kolmapäev", "Neljapäev", "Reede"]
        date_iter = 0
        more_stripped_list = []

        for i in range(0, len(stripped_list) - 1):
            if i < len(stripped_list):
                if any(day in stripped_list[i] for day in days):
                    self.dates.append(stripped_list[i])
                    date_iter += 1
                else:
                    more_stripped_list.append(stripped_list[i])

        return more_stripped_list

    def merge_est_eng_lines(self, more_stripped_list):
        formatted_list = []

        for i in range(0, len(more_stripped_list) - 1):
            if i % 2 != 0:
                before_price_match = re.search(BEFORE_PRICE_PATTERN, more_stripped_list[i - 1])
                price_match = re.search(PRICE_PATTERN, more_stripped_list[i - 1])
                new_line = \
                more_stripped_list[i-1][:before_price_match.end()].rstrip() \
                + " / " + more_stripped_list[i] + " - "
                if price_match is not None:
                    new_line += more_stripped_list[i-1][price_match.start():]
                formatted_list.append(new_line)

        return formatted_list

    def multiple_days_lists(self, formatted_list, STATIC_TEXT):
        list_of_lists = [[]]
        counter = 0
        for i in range(len(formatted_list)):
            if (i is 0):
                day_menu = [self.dates.pop(0)]
            if (i is 0) or (i % 6 is not 0):
                day_menu.append(formatted_list[i])
            else:
                day_menu.append(STATIC_TEXT)
                list_of_lists.append(day_menu)
                day_menu = [self.dates.pop(0)]
                day_menu.append(formatted_list[i])
        day_menu.append(STATIC_TEXT)
        list_of_lists.append(day_menu)
        del list_of_lists[0]
        return list_of_lists
