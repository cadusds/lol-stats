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
            dct["game_id"] = match_id.replace("BR1_", "")
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
            models.UniqueConstraint(
                fields=["summoner", "match_id"], name="unique_match"
            )
        ]


class Match(models.Model):
    game_id = models.CharField(max_length=250)
    game_creation = models.DateTimeField()
    game_start_timestamp = models.DateTimeField()
    game_end_timestamp = models.DateTimeField()
    game_duration = models.BigIntegerField
    game_mode = models.CharField(max_length=250)
    game_name = models.CharField(max_length=250)
    game_type = models.CharField(max_length=250)
    game_version = models.CharField(max_length=250)
    map_id = models.IntegerField()
    platform_id = models.CharField(max_length=250)
    queue_id = models.IntegerField()
    teams = models.JSONField()
    tournament_code = models.CharField(max_length=250)


class MatchParticipantBasicStats(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    game_id = models.ForeignKey(SummonerMatch, on_delete=models.CASCADE, null=False)
    team_position = models.CharField(max_length=200)
    deaths = models.IntegerField()
    assists = models.IntegerField()
    kills = models.IntegerField()
    double_kills = models.IntegerField()
    triple_kills = models.IntegerField()
    quadra_kills = models.IntegerField()
    penta_kills = models.IntegerField()
    first_blood_kill = models.BooleanField()
    first_blood_assist = models.BooleanField()
    first_tower_kill = models.BooleanField()
    first_tower_assist = models.BooleanField()
    largest_multi_kill = models.IntegerField()
    win = models.BooleanField()


class MatchParticipantStats(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    game_id = models.ForeignKey(SummonerMatch, on_delete=models.CASCADE, null=False)
    champion_name = models.CharField(max_length=250)
    total_damage_dealt = models.IntegerField()
    total_damage_dealt_to_champions = models.IntegerField()
    total_damage_taken = models.IntegerField()
    magic_damage_dealt = models.IntegerField()
    magic_damage_dealt_to_champions = models.IntegerField()
    magic_damage_taken = models.IntegerField()
    physical_damage_dealt = models.IntegerField()
    physical_damage_dealt_to_champions = models.IntegerField()
    physical_damage_taken = models.IntegerField()
    total_heal = models.IntegerField()
    total_minions_killed = models.IntegerField()
    total_time_spent_dead = models.IntegerField()
    true_damage_dealt = models.IntegerField()
    true_damage_dealt_to_champions = models.IntegerField()
    true_damage_taken = models.IntegerField()
    turrent_kills = models.IntegerField()
    turrent_takes = models.IntegerField()
    turrents_lost = models.IntegerField()
    vision_score = models.IntegerField()
    vision_wards_bought_in_game = models.IntegerField()
    wards_killed = models.IntegerField()
    wards_placed = models.IntegerField()
    gold_earned = models.IntegerField()
    gold_spent = models.IntegerField()
    longest_time_spent_living = models.IntegerField()
    time_played = models.IntegerField()
