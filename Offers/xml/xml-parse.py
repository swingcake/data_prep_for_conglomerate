from bs4 import BeautifulSoup

# read offer file
offer_xml = open("Offers_06062018.xml", 'r').read()

# make BeautifulSoup object
soup = BeautifulSoup(offer_xml, "lxml")

data = soup.find_all('metadata')

for datum in data:
    title = datum.find("field", {'name':"sbi.offers.title"}).text
    description = datum.find("field", {'name':"sbi.offers.description"}).text
    offer_text = datum.find("field", {'name':"sbi.offers.offertext"}).text
    is_online = datum.find("field", {'name':"sbi.offers.isonline"}).text
    category = datum.find("field", {'name':"sbi.offers.category"}).text
    start_date = datum.find("field", {'name':"sbi.offers.startdate"}).text
    end_date = datum.find("field", {'name':"sbi.offers.enddate"}).text

    print("title:" + title)
    print("description:" + description)
    print("offer_text:" + offer_text)
    print("is_online:" + is_online)
    print("category:" + category)
    print("start_date:" + start_date)
    print("end_date:" + end_date)