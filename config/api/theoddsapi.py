import requests
from datetime import datetime, timedelta
from sportsbetapp.models import Game, Bookmaker, Outcome
from uuid import uuid4
from requests.exceptions import RequestException
from django.utils.dateparse import parse_datetime

def get_sports(api_key):
    url = "https://api.the-odds-api.com/v4/sports"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    params = {
        "api_key": api_key,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        sports = []
        for sport_data in response_json:
            sport = {
                "key": sport_data["key"],
                "group": sport_data["group"],
                "title": sport_data["title"],
                "description": sport_data["description"],
                "active": sport_data["active"],
                "has_outrights": sport_data["has_outrights"],
            }
            sports.append(sport)
        return sports
    else:
        return []

##get upcoming games for game_details.html page


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
                game_obj = Game.objects.create(home_team=game['home_team'], away_team=game['away_team'], commence_time=game['commence_time'])
                for bookmaker in game['bookmakers']:
                    bookmaker_obj, created = Bookmaker.objects.get_or_create(title=bookmaker['title'])
                    for outcome in bookmaker['markets'][0]['outcomes']:
                        Outcome.objects.create(game=game_obj, bookmaker=bookmaker_obj, name=outcome['name'], price=outcome['price'])

        return upcoming_games


