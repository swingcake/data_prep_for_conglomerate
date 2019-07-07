import pandas as pd
import requests
import csv
from time import sleep
import random

def output_tuple(row):
    return (
        row['name'].replace(',', ''),
        row['formatted_address'].replace(',', ''),
        str(row['geometry']['location']['lat']),
        str(row['geometry']['location']['lng'])
    )

def search_output(search):
    if len(data['results']) == 0:
        print('No results found for {}.'.format(search))
    else:
        filename = search + '.csv'
        with open(filename, "w") as f:
            file_writer = csv.writer(f)
            file_writer.writerows(
                output_tuple(row)
                for row
                in data['results'])

        print('File successfully saved for "{}".'.format(search))

        sleep(random.randint(120, 150))

http_proxy = 'http://503070370:Test$444user@Uproxyggn.sbic.sbicard.com:8080'
https_proxy = 'https://503070370:Test$444user@Uproxyggn.sbic.sbicard.com:8080'

proxies = {
    'http'  : http_proxy,
    'https'  : https_proxy
}

API_KEY = 'your_api_key_here'

PLACES_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'

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
    elif status == 'ZERO_RESULTS':
        print('Zero results for "{}". Moving on..'.format(search))
        sleep(random.randint(120, 150))
    elif status == 'OVER_QUERY_LIMIT':
        print('Hit query limit! Try after a while. Could not complete "{}".'.format(search))
        break
    else:
        print(status)
        print('^ Status not okay, try again. Failed to complete "{}".'.format(search))
        break
