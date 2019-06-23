import pandas as pd
# import googlemaps
import requests
import csv
# import pprint as pp
from time import sleep
import random


def search_output(search):
    if len(data['results']) == 0:
        print('No results found for {}.'.format(search))

    else:

        # Create csv file
        filename = search + '.csv'
        f = open(filename, "w")

        size_of_json = len(data['results'])

        for i in range(size_of_json):
            name = data['results'][i]['name']
            address = data['results'][i]['formatted_address']
            latitude = data['results'][i]['geometry']['location']['lat']
            longitude = data['results'][i]['geometry']['location']['lng']

            f.write(name.replace(',', '') + ',' + address.replace(',', '') + ',' + str(latitude) + ',' + str(longitude) + '\n')

            # rows = [
                # data['results'][i]['name'],
                # data['results'][i]['formatted_address'],
                # data['results'][i]['geometry']['location']['lat'],
                # data['results'][i]['geometry']['location']['lng']
            # ]

            # print(row[1])

            # with open(filename, 'w', newline='') as f:
                # writer = csv.writer(f)
                # for row in rows:
                    # writer.writerow(row)

            # print(name)
            # print(address)
            # print(latitude)
            # print(longitude)
            # print('--')
        f.close()

        sleep(random.randint(3,11))


http_proxy = 'http://503070370:Test$444user@Uproxyggn.sbic.sbicard.com:8080'
https_proxy = 'https://503070370:Test$444user@Uproxyggn.sbic.sbicard.com:8080'

proxies = {
    'http'  : http_proxy,
    'https'  : https_proxy
}

API_KEY = 'your_api_key_here'

PLACES_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'


# Don't know how to implement this using requests
    # Define client
    # gmaps = googlemaps.Client(key=API_KEY)

    # Get the result through this function
    # search_result = gmaps.places(query='Starbucks, Chicago')


# Make dataframe
df = pd.read_csv('Merchant_Transaction.csv', usecols=[0, 1])

# Construct search query
search_query = df['Merchant_Name'].astype(str) + ' ' + df['City']
search_query = search_query.str.replace(' ', '+')

random.seed()

for search in search_query:
    search_req = 'query={}&key={}'.format(search, API_KEY)
    request = PLACES_URL + search_req

    # Place request and store data in 'data'
    result = requests.get(request, proxies=proxies, verify=False)
    data = result.json()

    status = data['status']

    if status == 'OK':
        search_output(search)
    elif status == 'OVER_QUERY_LIMIT':
        print('Hit query limit! Try after a while. Could not complete "{}".'.format(search))
        break
    else:
        print(status)
        print('^ Status not okay, try again. Failed to complete "{}".'.format(search))
        break