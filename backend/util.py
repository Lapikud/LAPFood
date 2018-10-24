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

def download_pdf(url, filepath):
    return urllib.request.urlretrieve(url, filepath)

def up_to_date_file_exists(path):
    if os.path.exists(path):
        modified_time = datetime.fromtimestamp(os.path.getmtime(path))
        now = datetime.now()
        difference = now - modified_time
        print(difference)
        if (difference.days < 1):
            return True

def wait_until_file_exists(path):
    while not os.path.exists(path):
        time.sleep(1)
    if os.path.isfile(path):
        return True

def get_subprocess(unix_process, args):
    return subprocess.Popen([unix_process, args[0], args[1]])