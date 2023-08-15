import os
import json
from django.utils.dateparse import parse_datetime
from .models import Game, Bookmaker, Market, Outcome 
from django.db import transaction

# @transaction.atomic rolls back any changes if at any point an exception occurs in the data loading process
@transaction.atomic

def load_data():
    directory = '/Users/ian/sportsbetapp/config/api' 
    for filename in os.listdir(directory):
        if filename.startswith('odds_') and filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                data = json.load(f)

            for item in data:
                try:
                    game = Game()
                    game.id = item['id']
                    game.sport_key = item['sport_key']
                    game.sport_title = item['sport_title']
                    game.commence_time = parse_datetime(item['commence_time'])
                    game.home_team = item['home_team']
                    game.away_team = item['away_team']
                    game.save()

                    for bookmaker_data in item['bookmakers']:
                        bookmaker = Bookmaker()
                        bookmaker.key = bookmaker_data['key']
                        bookmaker.title = bookmaker_data['title']
                        bookmaker.last_update = parse_datetime(bookmaker_data['last_update'])
                        bookmaker.game = game
                        bookmaker.save()

                        for market_data in bookmaker_data['markets']:
                            market = Market()
                            market.key = market_data['key']
                            market.last_update = parse_datetime(market_data['last_update'])
                            market.bookmaker = bookmaker
                            market.save()

                            for outcome_data in market_data['outcomes']:
                                outcome = Outcome()
                                outcome.name = outcome_data['name']
                                outcome.price = outcome_data['price']
                                outcome.market = market
                                outcome.save()

                except KeyError as e:
                    print(f"Missing key {e} in JSON data")