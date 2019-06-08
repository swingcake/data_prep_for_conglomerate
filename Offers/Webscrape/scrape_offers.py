from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
driver.get('https://www.sbicard.com/en/personal/offers.page#all-offers')

# html parsing
page_soup = BeautifulSoup(driver.page_source, 'lxml')

# grabs each offer
containers = page_soup.find_all("p", {'class':"white-strip"})

filename = "offers.csv"
f = open(filename, "w")

header = "offer-list\n"

f.write(header)

for container in containers:
    offer = container.span.text
    f.write(offer + "\n")

f.close()
driver.close()