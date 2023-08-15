import requests

def get_remaining_requests():
    url = f'https://api.the-odds-api.com/v4/sports/?apiKey=cff6cb1b3c6773cdd7053a1f54b84342'

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