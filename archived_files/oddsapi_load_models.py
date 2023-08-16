from django.core.management.base import BaseCommand
from sportsbetapp.models import Game, Bookmaker, Market, Outcome, TheOddsAPIData
from django.db import transaction
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Loads models from the API data stored in the TheOddsAPIData model'

    @transaction.atomic
    def handle(self, *args, **options):
        # Start populating models from stored API data
        self.populate_from_api_data()

    def populate_from_api_data(self):
        """Populate the database models from the stored API data."""
        num_games_loaded = 0  # keep track of number of games loaded

        for item in TheOddsAPIData.objects.all():
            data_list = item.data  # Expect this to be a list of games

            for data in data_list:
                if not data.get('id'):
                    print("ID not found, skipping this entry.")
                    continue

                away_team = data.get('away_team', 'Unknown Away Team')
                home_team = data.get('home_team', 'Unknown Home Team')
                print(f"Processing game between {away_team} and {home_team}")  # Debugging log
                game, created = self.process_game(data)
                if created:
                    num_games_loaded += 1

                self.process_bookmakers(data.get('bookmakers', []), game)

        print(f"{num_games_loaded} games were loaded into the database.")

    def process_game(self, data):
        return Game.objects.get_or_create(
            id=data.get('id'),
            defaults={
                'sport_key': data.get('sport_key'),
                'sport_title': data.get('sport_title'),
                'commence_time': parse_datetime(data.get('commence_time')),
                'home_team': data.get('home_team'),
                'away_team': data.get('away_team')
            }
        )

    def process_bookmakers(self, bookmakers_data, game):
        for bookmaker_data in bookmakers_data:
            print(f"Processing odds from {bookmaker_data.get('title')}")  # Debugging log

            bookmaker, created = Bookmaker.objects.get_or_create(
                key=bookmaker_data.get('key'),
                defaults={'title': bookmaker_data.get('title')}
            )

            self.process_markets(bookmaker_data.get('markets', []), bookmaker, game)

    def process_markets(self, markets_data, bookmaker, game):
        for market_data in markets_data:
            print(f"Processing market type: {market_data.get('key')}")  # Debugging log

            market, created = Market.objects.get_or_create(
                key=market_data.get('key'),
                defaults={
                    'last_update': parse_datetime(market_data.get('last_update')),
                    'bookmaker': bookmaker
                }
            )

            self.process_outcomes(market_data.get('outcomes', []), market, game, bookmaker)

    def process_outcomes(self, outcomes_data, market, game, bookmaker):
        for outcome_data in outcomes_data:
            print(f"Inserting/Updating odds for outcome: {outcome_data.get('name')} with price: {outcome_data.get('price')}")  # Debugging log

            Outcome.objects.get_or_create(
                name=outcome_data.get('name'),
                defaults={
                    'price': outcome_data.get('price'),
                    'market': market,
                    'game': game,
                    'bookmaker': bookmaker
                }
            )
