import requests
from datetime import datetime, timedelta
from sportsbetapp.models import Game

##this function currently fetches from the sports/odds endpoint, and populates data into models.
def get_upcoming_games():
    print("get_upcoming_games called")
    url = "https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us&markets=h2h&apiKey=cff6cb1b3c6773cdd7053a1f54b84342"

    try:
        response = requests.get(url)
        print(f"API response status code: {response.status_code}")
        data = response.json()
        print(f"API response data: {data}")
    except Exception as e:
        print(f"Failed to fetch data: {str(e)}")
        return None

    if response.status_code == 200:
        now = datetime.now()
        threshold = now + timedelta(hours=72)

        upcoming_games = []
        for game in data:
            commence_time = game['commence_time'].replace("Z", "")  # Remove the 'Z' character
            if datetime.strptime(commence_time, "%Y-%m-%dT%H:%M:%S") < threshold:
                upcoming_games.append(game)

        upcoming_games.sort(key=lambda x: x['commence_time'])  # Sort by event start time

        for game in upcoming_games:
            Game.objects.create(home_team=game['home_team'], away_team=game['away_team'], commence_time=game['commence_time'])
            print(f"Game object created: {game}")
                # Check the usage quota
            print('Remaining requests', response.headers['x-requests-remaining'])
            print('Used requests', response.headers['x-requests-used'])

        return upcoming_games

