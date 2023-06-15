from typing import Iterable, Optional
from django.db import models
from collector.api.league_of_legends_api import LeagueOfLegendsAPI


class SummonerManager(models.Manager):
    def create(self, summoner_name: str):
        summonner_data = LeagueOfLegendsAPI().get_summoner(summoner_name)
        return super().create(**summonner_data)


class Summoner(models.Model):
    puuid = models.CharField(primary_key=True, editable=False, max_length=250)
    summoner_id = models.CharField(max_length=250)
    account_id = models.CharField(max_length=250)
    name = models.CharField(max_length=250, unique=True)
    profile_icon_id = models.CharField(max_length=250)
    revision_date = models.DateTimeField()
    summoner_level = models.IntegerField()

    objects = SummonerManager()


class SummonerMatchManager(models.Manager):
    def create_all_matchs_by_puuid(self, puuid):
        matchs_data = LeagueOfLegendsAPI().get_all_matchs_by_summoner_puuid(puuid)
        matchs = list()
        summoner = Summoner.objects.get(puuid=puuid)
        for dct in matchs_data:
            dct["summoner"] = summoner
            match_id = dct["match_id"]
            dct["game_id"] = match_id.replace("BR1_","")
            match, _ = self.update_or_create(**dct)
            matchs.append(match)
        return matchs


class SummonerMatch(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    match_id = models.CharField(max_length=250)
    game_id = models.CharField(max_length=10)

    objects = SummonerMatchManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["summoner", "match_id"], name="unique_match")
        ]

    # def save(self,*args,**kwargs) -> None:
    #     self.game_id = int(str(self.match_id).replace("BR1_",""))
    #     return super(SummonerMatch,self).save(*args,**kwargs)