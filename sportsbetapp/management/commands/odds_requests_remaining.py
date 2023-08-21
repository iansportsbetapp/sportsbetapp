from django.core.management.base import BaseCommand
import requests
from decouple import config
import os

class Command(BaseCommand):
    help = 'Fetches the remaining odds requests'

    def handle(self, *args, **kwargs):
        api_key = config('ODDS_API')
        url = f'https://api.the-odds-api.com/v4/sports/?apiKey={api_key}'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            remaining_requests = int(response.headers.get('x-requests-remaining', 0))
            self.stdout.write(self.style.SUCCESS(f'Remaining requests: {remaining_requests}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to get remaining requests: status_code {response.status_code}, response body {response.text}'))