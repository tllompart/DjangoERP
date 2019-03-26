

from django.db import models

# Create your models here.


class Party(models.Model):
    name = models.CharField(max_length=32)
    full_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=9)
    mobile = models.CharField(max_length=9)
    fax = models.CharField(max_length=9)
    email = models.CharField(max_length=60)
    website = models.CharField(max_length=60)


class PartyCategory(models.Model):
    name = models.CharField(max_length=32)
