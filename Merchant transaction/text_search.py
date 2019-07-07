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
        row: Mapping[str, Any]
) -> Tuple[str, str, str, str]:
    return (
        row['name'].replace(',', ''),
        row['formatted_address'].replace(',', ''),
        str(row['geometry']['location']['lat']),
        str(row['geometry']['location']['lng'])
    )

def with_csv_writer(name: str, action: Callable)->None:
    with open(name + '.csv', "w", newline='') as f:
        action(csv.writer(f))

def output_search_results(
        writer: csv.Writer, 
        search_name: str, 
        results: Iterable[Mapping[str, Any]], 
        next_token: str
) -> bool:
    writer.writerows(
        output_tuple(row)
        for row
        in results)

    print('Successfully wrote page for "{}".'.format(search_name))
    
    if next_token:
        data = get_data(page = next_token)
        return handle_response(search_name, data, functools.partial(output_search_results, writer))
    else:
        return True

def output_search_results_with_new_writer(
        search_name: str, 
        results: Iterable[Mapping[str, Any]], 
        next_token: str
) -> bool:
    with open(search_name + '.csv', "w", newline='') as f:
        return output_search_results(
                csv.writer(f),
                search_name, 
                results, 
                next_token
            )

def get_data(
        query: str = '', 
        page: str = ''
) -> Mapping[str, Any]:
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

def handle_response(
        search_name: str, 
        data: Mapping[str, Any], 
        success_handler: Callable[[str, Iterable[Mapping[str, Any]], str], bool] = output_search_results_with_new_writer
) -> bool:
    status = data['status']

    if status == 'OK' and len(data['results']):
        return success_handler(
            search_name,
            data['results'], 
            data['next_page_token'] if 'next_page_token' in data else '', 
        )
    elif status == 'ZERO_RESULTS': # or !len(data['results]) ?
        print('Zero results for "{}". Moving on..'.format(search))
        return True
    elif status == 'OVER_QUERY_LIMIT':
        print('Hit query limit! Try after a while. Could not complete "{}".'.format(search))
        return False
    else:
        print(status)
        print('^ Status not okay, try again. Failed to complete "{}".'.format(search))
        return False



# Make dataframe
source_data = pd.read_csv('Merchant_Transaction.csv', usecols=[0, 1])

for row in source_data:
    search = "{}+{}".format(str(row['Merchant_Name']), df['City']).replace(' ', '+')

    data = get_data(query = search)
    if handle_response(search, data):
        sleep(150)
    else:
        break


