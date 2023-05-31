from django.db import models

# member model. not in use until login functionality complete.
class Member(models.Model):
  email = models.EmailField(max_length=125)
  firstname = models.CharField(max_length=125)
  lastname = models.CharField(max_length=125)
  phone = models.PositiveBigIntegerField()

# this model stores data for events 
class Game(models.Model):
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    commence_time = models.DateTimeField() 
    # Include any other fields that you want