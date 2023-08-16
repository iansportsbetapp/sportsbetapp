from ...models import Game, Bookmaker, Market, Outcome, TheOddsAPIData
from django.db import transaction

@transaction.atomic
def populate_from_api_data():
    for item in TheOddsAPIData.objects.all():
        data = item.data  # assuming data is stored in a JSONField or similar

        try:
            game, created = Game.objects.get_or_create(
                id=data['id'],
                defaults={
                    'sport_key': data['sport_key'],
                    'sport_title': data['sport_title'],
                    'commence_time': parse_datetime(data['commence_time']),
                    'home_team': data['home_team'],
                    'away_team': data['away_team']
                }
            )

            for bookmaker_data in data['bookmakers']:
                bookmaker, created = Bookmaker.objects.get_or_create(
                    key=bookmaker_data['key'],
                    defaults={
                        'title': bookmaker_data['title'],
                        'last_update': parse_datetime(bookmaker_data['last_update']),
                        'game': game
                    }
                )

                for market_data in bookmaker_data['markets']:
                    market, created = Market.objects.get_or_create(
                        key=market_data['key'],
                        defaults={
                            'last_update': parse_datetime(market_data['last_update']),
                            'bookmaker': bookmaker
                        }
                    )

                    for outcome_data in market_data['outcomes']:
                        Outcome.objects.get_or_create(
                            name=outcome_data['name'],
                            defaults={
                                'price': outcome_data['price'],
                                'market': market
                            }
                        )

        except KeyError as e:
            print(f"Missing key {e} in API data")