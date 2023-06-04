import json
from django.http import JsonResponse

def get_upcoming_games(selected_sport):
    upcoming_games = []

    # Construct the JSON file name based on the selected sport
    json_file_name = f'odds_{selected_sport}.json'

    # Load the JSON data from the file
    with open(json_file_name, 'r') as file:
        data = json.load(file)

    # Process the data from the JSON file and add it to the upcoming_games list
    for game in data:
        # Assuming the JSON data has keys like 'home_team', 'away_team', 'commence_time'
        home_team = game['home_team']
        away_team = game['away_team']
        commence_time = game['commence_time']

        # Add the game details to the upcoming_games list
        upcoming_games.append({
            'home_team': home_team,
            'away_team': away_team,
            'commence_time': commence_time
        })

    # Return the upcoming_games list as JSON response
    return JsonResponse(upcoming_games, safe=False)