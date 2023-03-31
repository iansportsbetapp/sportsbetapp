from django.db import models

# Create your models here.
class Member(models.Model):
  email = models.EmailField(max_length=125)
  firstname = models.CharField(max_length=125)
  lastname = models.CharField(max_length=125)
  phone = models.PositiveBigIntegerField()