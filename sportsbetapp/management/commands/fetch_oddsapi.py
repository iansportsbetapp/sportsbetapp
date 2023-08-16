from django.core.management.base import BaseCommand
from sportsbetapp.models import TheOddsAPIData
import requests
from decouple import config
from django.utils import timezone

class Command(BaseCommand):
    help = 'Fetches data from the Odds API and stores it in TheOddsAPIData model'

    def handle(self, *args, **options):
        # Start fetching and storing data
        self.get_sports_json()
        
        # Load sports JSON data from the database
        sports_json_data_entry = TheOddsAPIData.objects.latest('created_at')
        sports_json_data = sports_json_data_entry.data

        # Retrieve and save odds JSON data for each sport
        self.get_odds_json(sports_json_data)
        
    def get_sports_json(self):
        """Retrieves sports JSON data from the API and saves it to the database."""
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

            # Save the sports JSON data to the database
            TheOddsAPIData.objects.create(data=sports_json_data, created_at=timezone.now())

    def get_odds_json(self, sports_json):
        """Retrieves odds JSON data for active sports from the API and saves it to the database."""
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

                    # Save the odds JSON data to the database
                    TheOddsAPIData.objects.create(data=odds_json_data, created_at=timezone.now())
