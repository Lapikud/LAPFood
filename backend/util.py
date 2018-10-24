from html.parser import HTMLParser
import urllib.request
import subprocess
import os
import time
from datetime import datetime



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

def download_pdf(url, file_path):
    return urllib.request.urlretrieve(url, file_path)

def up_to_date_file_exists(data_path, file_path):
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    if os.path.exists(data_path + file_path):
        modified_time = datetime.fromtimestamp(os.path.getmtime(data_path + file_path))
        now = datetime.now()
        difference = now - modified_time
        if (difference.days < 1):
            return True

def wait_until_file_exists(data_path, file_path):
    while not os.path.exists(data_path + file_path):
        time.sleep(1)
    if os.path.isfile(data_path + file_path):
        return True

def get_subprocess(unix_process, args):
    return subprocess.Popen([unix_process, args[0], args[1]])