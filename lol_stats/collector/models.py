from django.db import models


class Summoners(models.Model):

    summoner_id = models.CharField(max_length=250)
    account_id = models.CharField(max_length=250)
    puuid = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    profile_icon_id = models.CharField(max_length=250)
    revision_date = models.DateTimeField()
    summoner_level = models.IntegerField()

