from django.db import models
from collector.api.league_of_legends_api import LeagueOfLegendsAPI
from concurrent.futures import ThreadPoolExecutor as Thread


class SummonerManager(models.Manager):
    def create_summoner_by_name(self, name: str):
        summonner_data = LeagueOfLegendsAPI().get_summoner(name)
        return self.create(**summonner_data)


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
        summoner = Summoner.objects.get(puuid=puuid)
        for dct in matchs_data:
            dct["summoner"] = summoner
            match_id = dct["match_id"]
            dct["game_id"] = match_id.replace("BR1_", "")
            self.update_or_create(**dct)
        return SummonerMatch.objects.filter(summoner=summoner)

    def create_all_matchs_stats_by_puuid(self, puuid):
        summoner = Summoner.objects.get(puuid=puuid)
        summoner_matchs = SummonerMatch.objects.filter(summoner=summoner)
        matchs = list(
            map(lambda summoner_match: summoner_match.match_id, summoner_matchs)
        )
        with Thread(max_workers=4) as executor:
            list_data = list(executor.map(LeagueOfLegendsAPI().get_match_stats, matchs))
        results = list()
        for data in list_data:
            results.append(Match.objects.create_match_object_with_match_data(data))
        return results
        # executor.map(
        #     lambda data: MatchParticipantBasicStats.objects.create_match_participant_basic_stats_object_with_match_data(
        #         data, puuid
        #     ),
        #     list_data,
        # )
        # executor.map(
        #     lambda data: MatchParticipantStats.objects.create_match_participant_stats_object_with_match_data(
        #         data, puuid
        #     ),
        #     matchs_data,
        # )


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


class MatchManager(models.Manager):
    def get_match_stats_data(self, match_data: dict) -> dict:
        fields = [x.name for x in Match._meta.fields if x.name != "id"]
        dct = {x: match_data[x] for x in fields}
        return dct

    def create_match_object_with_match_data(self, match_data: dict) -> models.Model:
        data = self.get_match_stats_data(match_data)
        return self.update_or_create(**data)


class Match(models.Model):
    game_id = models.CharField(max_length=250)
    game_creation = models.CharField(max_length=250)
    game_start_timestamp = models.CharField(max_length=250)
    game_end_timestamp = models.CharField(max_length=250)
    game_duration = models.CharField(max_length=250)
    game_mode = models.CharField(max_length=250)
    game_name = models.CharField(max_length=250)
    game_type = models.CharField(max_length=250)
    game_version = models.CharField(max_length=250)
    map_id = models.IntegerField()
    platform_id = models.CharField(max_length=250)
    queue_id = models.IntegerField()
    teams = models.JSONField()
    tournament_code = models.CharField(max_length=250)

    objects = MatchManager()


class MatchParticipantBasicStatsManager(models.Manager):
    def get_match_participant_basic_stats_data(
        self, match_data: dict, puuid: str
    ) -> dict:
        match_data = list(
            filter(
                lambda participant: participant["puuid"] == puuid,
                match_data["participants"],
            )
        )[0]
        fields = [x.name for x in MatchParticipantBasicStats._meta.fields if x != "id"]
        dct = {x: match_data[x] for x in fields}
        return dct

    def create_match_participant_basic_stats_object_with_match_data(
        self, match_data: dict, puuid: str
    ) -> models.Model:
        data = self.get_match_participant_basic_stats_data(match_data, puuid)
        obj, _ = self.update_or_create(**data)
        return obj


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

    objects = MatchParticipantBasicStatsManager()


class MatchParticipantStatsManager(models.Manager):
    def get_match_participant_stats_data(self, match_data: dict, puuid: str) -> dict:
        data = list(
            filter(
                lambda participant: participant["puuid"] == puuid,
                match_data["participants"],
            )
        )[0]
        fields = [x.name for x in MatchParticipantStats._meta.fields if x != "id"]
        dct = {x: data[x] for x in fields}
        return dct

    def create_match_participant_stats_object_with_match_data(
        self, match_data: dict, puuid: str
    ) -> models.Model:
        data = self.get_match_participant_stats_data(match_data, puuid)
        obj, _ = self.update_or_create(**data)
        return obj


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

    objects = MatchParticipantStatsManager()


class MatchParticipantChampionStatsManager(models.Manager):
    def get_match_participant_champion_stats_data(
        self, match_data: dict, puuid: str
    ) -> dict:
        data = list(
            filter(
                lambda participant: participant["puuid"] == puuid,
                match_data["participants"],
            )
        )[0]
        fields = [
            x.name for x in MatchParticipantChampionStats._meta.fields if x != "id"
        ]
        dct = {x: data[x] for x in fields}
        return dct


class MatchParticipantChampionStats(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    game_id = models.ForeignKey(SummonerMatch, on_delete=models.CASCADE, null=False)
    champion_name = models.CharField(max_length=200)
    champ_experience = models.IntegerField()
    champ_level = models.IntegerField()
    items_purchased = models.IntegerField()
    item0 = models.IntegerField()
    item1 = models.IntegerField()
    item2 = models.IntegerField()
    item3 = models.IntegerField()
    item4 = models.IntegerField()
    item5 = models.IntegerField()
    item6 = models.IntegerField()
    spell1_casts = models.IntegerField()
    spell2_casts = models.IntegerField()
    spell3_casts = models.IntegerField()
    spell4_casts = models.IntegerField()
