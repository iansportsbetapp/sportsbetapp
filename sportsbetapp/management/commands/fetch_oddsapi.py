from django.core.management.base import BaseCommand
from sportsbetapp.models import Game, Bookmaker, Market, Outcome, Sport
import requests
from decouple import config
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Fetches data from the Odds API and stores it in the respective models'

    def handle(self, *args, **options):
        # Fetch and store sports data
        sports_json_data = self.get_sports_json()

        # Retrieve and save odds data for each sport
        self.get_and_save_odds_data(sports_json_data)
        
    def get_sports_json(self):
        """Retrieves sports JSON data from the API and saves it to the Sport model."""
        api_key = config('ODDS_API')
        sports_response = requests.get(
            'https://api.the-odds-api.com/v4/sports',
            params={
                "api_key": api_key,
                'all': 'true'
            }
        )

        sports_json_data = []
        if sports_response.status_code != 200:
            print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
        else:
            sports_json_data = sports_response.json()
            for sport in sports_json_data:
                Sport.objects.update_or_create(
                    key=sport['key'],
                    defaults={
                        'title': sport['title'],
                        'is_active': sport['active'],
                    }
                )
        return sports_json_data

    def get_and_save_odds_data(self, sports_json):
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
                    continue

                odds_json_data = odds_response.json()
                print(f'Number of events for sport {sport["key"]}:', len(odds_json_data))
                for game_data in odds_json_data:
                    game_instance, _ = Game.objects.update_or_create(
                        id=game_data["id"],
                        defaults={
                            'sport_key': game_data["sport_key"],
                            'sport_title': sport["title"],
                            'commence_time': game_data["commence_time"],
                            'home_team': game_data["home_team"],
                            'away_team': game_data["away_team"],
                        }
                    )
                    for bookmaker_data in game_data["bookmakers"]:
                        bookmaker_instance, _ = Bookmaker.objects.update_or_create(
                            key=bookmaker_data["key"],
                            defaults={'title': bookmaker_data["title"]}
                        )
                        for market_data in bookmaker_data["markets"]:
                            market_instance, _ = Market.objects.update_or_create(
                                key=market_data["key"],
                                defaults={
                                    'last_update': bookmaker_data["last_update"],
                                    'bookmaker': bookmaker_instance
                                }
                            )
                            for outcome_data in market_data["outcomes"]:
                                Outcome.objects.get_or_create(
                                    game=game_instance,
                                    bookmaker=bookmaker_instance,
                                    name=outcome_data["name"],
                                    price=outcome_data["price"],
                                    point=outcome_data.get("point", None)
                                )
