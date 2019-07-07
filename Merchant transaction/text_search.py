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
    with open(name + '.csv', "w", newline='') as f:
        action(csv.writer(f))

def output_search_results(search_name, results, next_token, writer):
    writer.writerows(
        output_tuple(row)
        for row
        in results)

    print('Successfully wrote page for "{}".'.format(search_name))
    
    if next_token:
        data = get_data(page = next_token)

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
source_data = pd.read_csv('Merchant_Transaction.csv', usecols=[0, 1])

for row in source_data:
    search = "{}+{}".format(str(row['Merchant_Name']), df['City']).replace(' ', '+')

    data = get_data(query = search)
    status = data['status']

    if status == 'OK' and len(data['results']):
        with_csv_writer(
            search,
            lambda w: output_search_results(search, 
                                            data['results'], 
                                            data['next_page_token'] if 'next_page_token' in data else '', 
                                            w)
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


