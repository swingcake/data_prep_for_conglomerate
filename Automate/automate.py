import csv
import time
from urllib.request import urlopen

with open('url_file.csv', 'r') as csvfile:
    urls = csv.reader(csvfile)
    for url in urls:
        page = urlopen(url[0]).read()
        time.sleep(120)
