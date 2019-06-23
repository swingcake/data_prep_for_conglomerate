'''
This is now deprecated. 
'''

import csv
import time
# import webbrowser
from urllib.request import urlopen


contents = []
with open('url_file.csv', 'r') as csvfile:
    urls = csv.reader(csvfile)
    for url in urls:
        contents.append(url)

for url in contents:
    # webbrowser.open(url[0])
    page = urlopen(url[0]).read()
    time.sleep(120)