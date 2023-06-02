import requests
from datetime import datetime, timedelta
from sportsbetapp.models import Game
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

def get_upcoming_games():
    print("get_upcoming_games called") 
    url = "https://api.the-odds-api.com/v4/sports/upcoming/odds/?apiKey=cff6cb1b3c6773cdd7053a1f54b84342" 
    # replace 'upcoming' and 'cff6cb1b3c6773cdd7053a1f54b84342' with actual values if they're placeholders
    
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
        
        upcoming_games = [game for game in data['data'] if datetime.strptime(game['commence_time'], "%Y-%m-%dT%H:%M:%SZ") < threshold]
        
        for game in upcoming_games:
            Game.objects.create(home_team=game['home_team'], away_team=game['away_team'], commence_time=game['commence_time'])  
            print(f"Game object created: {game}")
        
        return upcoming_games

