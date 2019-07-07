import pandas as pd
import requests
import csv
from time import sleep

# Config
proxies = {
    'http': 'http://503070370:Test$444user@Uproxyggn.sbic.sbicard.com:8080',
    'https': 'https://503070370:Test$444user@Uproxyggn.sbic.sbicard.com:8080',
}
API_KEY = 'your_api_key_here'
PLACES_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

def output_tuple(row):
    return (
        row['name'].replace(',', ''),
        row['formatted_address'].replace(',', ''),
        str(row['geometry']['location']['lat']),
        str(row['geometry']['location']['lng'])
    )

def with_csv_writer(name, action):
    with open(name + '.csv', "w") as f:
        action(csv.writer(f))

def output_search_results(search_name, results, writer):
    writer.writerows(
        output_tuple(row)
        for row
        in results)
    print('File successfully saved for "{}".'.format(search_name))

def get_data(query = '', page = ''):
    use_query = not page
    return requests.get(
        '{}?{}={}&key={}'.format(
            PLACES_URL, 
            'query' if use_query else 'pagetoken', 
            query if use_query else page, 
            API_KEY
        ), 
        proxies=proxies, 
        verify=False
    ).json()

# Make dataframe
df = pd.read_csv('Merchant_Transaction.csv', usecols=[0, 1])

# Construct search query
search_query = df['Merchant_Name'].astype(str) + ' ' + df['City']
search_query = search_query.str.replace(' ', '+')


for search in search_query:
    data = get_data(query = search)

    status = data['status']

    if status == 'OK' and len(data['results']):
        with_csv_writer(
            search,
            lambda w: output_search_results(search, data['results'], w)
        )
    elif status == 'ZERO_RESULTS': # or !len(data['results]) ?
        print('Zero results for "{}". Moving on..'.format(search))
    elif status == 'OVER_QUERY_LIMIT':
        print('Hit query limit! Try after a while. Could not complete "{}".'.format(search))
        break
    else:
        print(status)
        print('^ Status not okay, try again. Failed to complete "{}".'.format(search))
        break

    sleep(150)


