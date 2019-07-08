import pandas as pd
import requests
import csv
from time import sleep
import functools
from typing import Any, Callable, Iterable, Mapping, Tuple

# Config
proxies = {
    'http': 'http://503070370:Test$444user@Uproxyggn.sbic.sbicard.com:8080',
    'https': 'https://503070370:Test$444user@Uproxyggn.sbic.sbicard.com:8080',
}
API_KEY = 'your_api_key_here'
PLACES_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

def output_tuple(
        row: Mapping[str, Any],
        search_name: Tuple[str, str]
) -> Tuple[str, str, str, str, str, str]:
    return (
        search_name[0].replace(',', ''),
        search_name[1].replace(',', ''),
        row['name'].replace(',', ''),
        row['formatted_address'].replace(',', ''),
        str(row['geometry']['location']['lat']),
        str(row['geometry']['location']['lng'])
    )

def output_search_results(
        writer: csv.Writer, 
        search_name: Tuple[str], 
        results: Iterable[Mapping[str, Any]], 
        next_token: str
) -> bool:
    writer.writerows(
        output_tuple(row)
        for row
        in results)

    print('Successfully wrote page for "{}, {}".'.format(*search_name))
    
    if next_token:
        data = get_data(page = next_token)65d623059af08d23066104e4f3bf2659f4732900
        return handle_response(search_name, data, functools.partial(output_search_results, writer))
    else:
        return True

def output_search_results_with_new_writer(
        search_name: Tuple[str, str], 
        results: Iterable[Mapping[str, Any]], 
        next_token: str
) -> bool:
    with open('{}_{}.csv'.format(*search_name), 'w', encoding='utf-8-sig', newline='') as f:
        return output_search_results(
                csv.writer(f),
                search_name, 
                results, 
                next_token
            )

def get_data(
        query: str = '', 
        page: str = '',
        latitude: str = '',
        longitude: str = '',
        url: str = PLACES_URL
) -> Mapping[str, Any]:
    key = 'query'
        if query
        else ('pagetoken' if page else 'latlng')
    value = query
        if query
        else (page if page else '{},{}'.format(latitude, longitude))
    return requests.get(
        '{}?{}={}&key={}'.format(url, key, value, API_KEY), 
        proxies=proxies, 
        verify=False
    ).json()

def handle_response(
        search_name: Tuple[str, str], 
        data: Mapping[str, Any], 
        success_handler: Callable[[Tuple[str, str], Iterable[Mapping[str, Any]], str], bool] = output_search_results_with_new_writer
) -> bool:
    status = data['status']

    if status == 'OK' and len(data['results']):
        return success_handler(
            search_name,
            data['results'], 
            data['next_page_token'] if 'next_page_token' in data else '', 
        )
    elif status == 'ZERO_RESULTS': # or !len(data['results]) ?
        print('Zero results for "{}, {}". Moving on..'.format(*search_name))
        return True
    elif status == 'OVER_QUERY_LIMIT':
        print('Hit query limit! Try after a while. Could not complete "{}, {}".'.format(search_name))
        return False
    else:
        print(status)
        print('^ Status not okay, try again. Failed to complete "{}, {}".'.format(*search_name))
        return False



# Make dataframe
source_data = pd.read_csv('Merchant_Transaction.csv', usecols=[0, 1])

for row in source_data.itertuples():
    search_name = (str(row['Merchant_Name']), str(row['City']))

    data = get_data(query = "{} {}".format(*search_name))
    if handle_response(search_name, data):
        sleep(150)
    else:
        break


