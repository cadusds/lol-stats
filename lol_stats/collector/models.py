from django.db import models
from collector.api.league_of_legends_api import LeagueOfLegendsAPI


class SummonerManager(models.Manager):

    def create(self, summoner_name:str):
        summonner_data = LeagueOfLegendsAPI().get_summoner(summoner_name)
        return super().create(**summonner_data)

class Summoner(models.Model):

    summoner_id = models.CharField(max_length=250)
    account_id = models.CharField(max_length=250)
    puuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=250, unique=True)
    profile_icon_id = models.CharField(max_length=250)
    revision_date = models.DateTimeField()
    summoner_level = models.IntegerField()

    objects = SummonerManager()

class MatchManager(models.Manager):
    
    def create_all_matchs_by_puuid(self,puuid):
        matchs_data = LeagueOfLegendsAPI().get_all_matchs_by_summoner_puuid(puuid)
        matchs = list()
        for dct in matchs_data:
            summoner = Summoner.objects.get(puuid=puuid)
            dct["puuid"] = summoner
            match = self.create(**dct)
            matchs.append(match)
        return matchs    
        
class Match(models.Model):
    
    puuid = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    match_id = models.CharField(max_length=250)
    
    objects = MatchManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['puuid', 'match_id'], name='unique_match')
        ]