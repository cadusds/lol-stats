from django.db import models


class SummonerManager(models.Manager):

    def create(self, summoner_name:str):
        from collector.api.league_of_legends_api import LeagueOfLegendsAPI
        summonner_data = LeagueOfLegendsAPI().get_summoner(summoner_name)
        return super().create(**summonner_data)

class Summoner(models.Model):

    summoner_id = models.CharField(max_length=250)
    account_id = models.CharField(max_length=250)
    puuid = models.CharField(max_length=250)
    name = models.CharField(max_length=250, unique=True)
    profile_icon_id = models.CharField(max_length=250)
    revision_date = models.DateTimeField()
    summoner_level = models.IntegerField()

    objects = SummonerManager()