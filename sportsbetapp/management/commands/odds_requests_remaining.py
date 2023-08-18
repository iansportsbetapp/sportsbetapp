import requests
from decouple import config
import os


def get_remaining_requests():
    api_key = os.getenv("THE_ODDS")
    url = f'https://api.the-odds-api.com/v4/sports/?apiKey={api_key}'


    response = requests.get(url)

    if response.status_code == 200:
        remaining_requests = int(response.headers.get('x-requests-remaining', 0))
        return remaining_requests
    else:
        print(f'Failed to get remaining requests: status_code {response.status_code}, response body {response.text}')
        return None

# Call the function
remaining_requests = get_remaining_requests()
if remaining_requests is not None:
    print('Remaining requests:', remaining_requests)