from bs4 import BeautifulSoup

# read offer file
offer_xml = open("Offers_06062018.xml", 'r')

# make BeautifulSoup object
soup = BeautifulSoup(offer_xml, "lxml")

data = soup.find_all('metadata')

filename = "offers_xml.csv"
f = open(filename, "w")

header = "title, description, offer_text, is_online, category, start_date, end_date\n"

f.write(header)

for datum in data:
    if datum.find("field", {'name':"multinational_conglomerate.offers.title"}) == None:
        title = ""
    else:
        title = datum.find("field", {'name':"multinational_conglomerate.offers.title"}).text

    if datum.find("field", {'name':"multinational_conglomerate.offers.description"}) == None:
        description = ""
    else:
        description = datum.find("field", {'name':"multinational_conglomerate.offers.description"}).text

    if datum.find("field", {'name':"multinational_conglomerate.offers.offertext"}) == None:
        offer_text = ""
    else:
        offer_text = datum.find("field", {'name':"multinational_conglomerate.offers.offertext"}).text

    if datum.find("field", {'name':"multinational_conglomerate.offers.isonline"}) == None:
        is_online = ""
    else:
        is_online = datum.find("field", {'name':"multinational_conglomerate.offers.isonline"}).text

    if datum.find("field", {'name':"multinational_conglomerate.offers.category"}) == None:
        category = ""
    else:
        category = datum.find("field", {'name':"multinational_conglomerate.offers.category"}).text

    if datum.find("field", {'name':"multinational_conglomerate.offers.startdate"}) == None:
        start_date = ""
    else:
        start_date = datum.find("field", {'name':"multinational_conglomerate.offers.startdate"}).text

    if datum.find("field", {'name':"multinational_conglomerate.offers.enddate"}) == None:
        end_date = ""
    else:
        end_date = datum.find("field", {'name':"multinational_conglomerate.offers.enddate"}).text

    f.write(title + "," + description.replace( ",", " ") + "," + offer_text.replace( ",", " ") + "," + is_online + "," + category.replace( ",", "|") + "," + start_date + "," + end_date + "\n")

f.close()

    # description = datum.find("field", {'name':"multinational_conglomerate.offers.description"}).text
    # offer_text = datum.find("field", {'name':"multinational_conglomerate.offers.offertext"}).text
    # is_online = datum.find("field", {'name':"multinational_conglomerate.offers.isonline"}).text
    # category = datum.find("field", {'name':"multinational_conglomerate.offers.category"}).text
    # start_date = datum.find("field", {'name':"multinational_conglomerate.offers.startdate"}).text
    # end_date = datum.find("field", {'name':"multinational_conglomerate.offers.enddate"}).text

    # print("title:" + title)
    # print("description:" + description)
    # print("offer_text:" + offer_text)
    # print("is_online:" + is_online)
    # print("category:" + category)
    # print("start_date:" + start_date)
    # print("end_date:" + end_date)
