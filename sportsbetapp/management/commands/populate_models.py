from django.core.management.base import BaseCommand
from sportsbetapp.models import Game, Bookmaker, Outcome, Market
import json
import os

class Command(BaseCommand):
    help = 'Populates the database with Game, Bookmaker, and Outcome objects from a JSON file'

    def handle(self, *args, **options):
        directory = '/Users/ian/sportsbetapp/config/api/'
   
        for filename in os.listdir(directory):
            if filename.endswith('.json') and filename.startswith('odds_'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    self.populate_models(data)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with Game, Bookmaker, and Outcome objects'))

    def populate_models(self, data):
        for game_data in data:
            game = Game(
                id=game_data['id'],
                sport_key=game_data['sport_key'],
                sport_title=game_data['sport_title'],
                commence_time=game_data['commence_time'],
                home_team=game_data['home_team'],
                away_team=game_data['away_team'],
            )
            game.save()

            bookmakers_data = game_data.get('bookmakers', [])

            for bookmaker_data in bookmakers_data:
                bookmaker, created = Bookmaker.objects.get_or_create(
                    key=bookmaker_data['key'], defaults={'title': bookmaker_data['title']}
                )

                markets_data = bookmaker_data.get('markets', [])

                for market_data in markets_data:
                    market, created = Market.objects.get_or_create(
                        key=market_data['key'],
                        defaults={'last_update': market_data['last_update'], 'bookmaker': bookmaker},
                    )

                    outcomes_data = market_data.get('outcomes', [])

                    for outcome_data in outcomes_data:
                        outcome, created = Outcome.objects.get_or_create(
                            game=game,
                            bookmaker=bookmaker,
                            name=outcome_data['name'],
                            defaults={'price': outcome_data['price'], 'point': outcome_data.get('point')},
                        )
                        if not created:
                            outcome.price = outcome_data['price']
                            outcome.point = outcome_data.get('point')
                            outcome.save()