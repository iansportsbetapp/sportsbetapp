import requests
import json
from decouple import config



def get_sports_json():
    api_key = config('ODDS_API')
    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports',
        params={
            "api_key": api_key,
            'all': 'true'
        }
    )
    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
    else:
        sports_json_data = sports_response.json()
        print('List of in season sports:', sports_json_data)

        # Save the sports JSON data to a file
        with open('api/sports.json', 'w') as file:
            json.dump(sports_json_data, file)


def get_odds_json(sports_json):
    api_key = config('ODDS_API')
    for sport in sports_json:
        if sport['active']:
            odds_response = requests.get(
                f"https://api.the-odds-api.com/v4/sports/{sport['key']}/odds",
                params={
                    'api_key': api_key,
                    'regions': 'us,us2',
                    'markets': 'h2h',
                    'oddsFormat': 'decimal',
                }
            )

            if odds_response.status_code != 200:
                print(f'Failed to get odds for sport {sport["key"]}: status_code {odds_response.status_code}, response body {odds_response.text}')
            else:
                odds_json_data = odds_response.json()
                print(f'Number of events for sport {sport["key"]}:', len(odds_json_data))
                print(odds_json_data)

                # Save the odds JSON data to a file
                with open(f'api/odds_{sport["key"]}.json', 'w') as file:
                    json.dump(odds_json_data, file)

# Retrieve and save sports JSON data
get_sports_json()

# Load sports JSON data from file
with open('api/sports.json', 'r') as file:
    sports_json_data = json.load(file)

# Retrieve and save odds JSON data for each sport
get_odds_json(sports_json_data)
