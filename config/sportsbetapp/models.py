from django.db import models

# member model. not in use until login functionality complete.
class Member(models.Model):
  email = models.EmailField(max_length=125)
  firstname = models.CharField(max_length=125)
  lastname = models.CharField(max_length=125)
  phone = models.PositiveBigIntegerField()

class Game(models.Model):
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    commence_time = models.DateTimeField()

class Bookmaker(models.Model):
    title = models.CharField(max_length=200)

class Outcome(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='outcomes')
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE, related_name='outcomes')
    name = models.CharField(max_length=200)  # Team name
    price = models.FloatField()
    point = models.FloatField(null=True, blank=True)  # Optional field for spreads