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


class MatchManager(models.Manager):
    def get_match_stats_data(self, match_data: dict) -> dict:
        fields = [x.name for x in Match._meta.fields if x.name != "game"]
        dct = {x: match_data[x] for x in fields}
        return dct

    def create_match_object_with_match_data(self, match_data: dict) -> models.Model:
        data = self.get_match_stats_data(match_data)
        return self.update_or_create(**data)


class Match(models.Model):
    game_id = models.CharField(max_length=250, primary_key=True)
    game_creation = models.CharField(max_length=250, null=True)
    game_start_timestamp = models.CharField(max_length=250, null=True)
    game_end_timestamp = models.CharField(max_length=250, null=True)
    game_duration = models.CharField(max_length=250, null=True)
    game_mode = models.CharField(max_length=250, null=True)
    game_name = models.CharField(max_length=250, null=True)
    game_type = models.CharField(max_length=250, null=True)
    game_version = models.CharField(max_length=250, null=True)
    map_id = models.IntegerField(null=True)
    platform_id = models.CharField(max_length=250, null=True)
    queue_id = models.IntegerField(null=True)
    teams = models.JSONField(null=True)
    tournament_code = models.CharField(max_length=250, null=True)

    objects = MatchManager()


class SummonerMatchManager(models.Manager):
    def create_all_matchs_by_puuid(self, puuid):
        matchs_data = LeagueOfLegendsAPI().get_all_matchs_by_summoner_puuid(puuid)
        summoner = Summoner.objects.get(puuid=puuid)
        for dct in matchs_data:
            dct["summoner"] = summoner
            match_id = dct["match_id"]
            dct["game_id"] = match_id.replace("BR1_", "")
            match, _ = Match.objects.get_or_create(game_id=dct["game_id"])
            del dct["game_id"]
            dct["game"] = match
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
        for data in list_data:
            Match.objects.create_match_object_with_match_data(data)
            MatchParticipantBasicStats.objects.create_match_participant_basic_stats_object_with_match_data(
                data, summoner.puuid
            )
            MatchParticipantChampionStats.objects.create_match_participant_champion_stats_object_with_match_data(
                data, summoner.puuid
            )
            MatchParticipantStats.objects.create_match_participant_stats_object_with_match_data(
                data, summoner.puuid
            )
        return {"status": "ok"}


class SummonerMatch(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    match_id = models.CharField(max_length=250)
    game = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)

    objects = SummonerMatchManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["summoner", "match_id"], name="unique_match"
            )
        ]


class MatchParticipantBasicStatsManager(models.Manager):
    def get_match_participant_basic_stats_data(
        self, match_data: dict, puuid: str
    ) -> dict:
        participant_stats = list(
            filter(
                lambda participant: participant["puuid"] == puuid,
                match_data["participants"],
            )
        )[0]
        participant_stats = LeagueOfLegendsAPI._format_keys(participant_stats)
        fields = [
            x.name
            for x in MatchParticipantBasicStats._meta.fields
            if x.name not in ["id", "summoner", "game"]
        ]
        match = Match.objects.get(game_id=match_data["game_id"])
        summoner = Summoner.objects.get(puuid=puuid)
        dct = {x: participant_stats[x] for x in fields}
        dct["summoner"] = summoner
        dct["game"] = match
        return dct

    def create_match_participant_basic_stats_object_with_match_data(
        self, match_data: dict, puuid: str
    ) -> models.Model:
        data = self.get_match_participant_basic_stats_data(match_data, puuid)
        return self.update_or_create(**data)


class MatchParticipantBasicStats(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Match, on_delete=models.CASCADE, null=False)
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
        data = LeagueOfLegendsAPI._format_keys(data)
        fields = [
            x.name
            for x in MatchParticipantStats._meta.fields
            if x.name not in ["id", "summoner", "game"]
        ]
        dct = {x: data[x] for x in fields}
        match = Match.objects.get(game_id=match_data["game_id"])
        summoner = Summoner.objects.get(puuid=puuid)
        dct["game"], dct["summoner"] = match, summoner
        return dct

    def create_match_participant_stats_object_with_match_data(
        self, match_data: dict, puuid: str
    ) -> models.Model:
        data = self.get_match_participant_stats_data(match_data, puuid)
        return self.update_or_create(**data)


class MatchParticipantStats(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Match, on_delete=models.CASCADE, null=False)
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
    turret_kills = models.IntegerField()
    turret_takedowns = models.IntegerField()
    turrets_lost = models.IntegerField()
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
        data = LeagueOfLegendsAPI._format_keys(data)
        fields = [
            x.name
            for x in MatchParticipantChampionStats._meta.fields
            if x.name not in ["id", "summoner", "game"]
        ]
        dct = {x: data[x] for x in fields}
        match = Match.objects.get(game_id=match_data["game_id"])
        summoner = Summoner.objects.get(puuid=puuid)
        dct["game"], dct["summoner"] = match, summoner
        return dct

    def create_match_participant_champion_stats_object_with_match_data(
        self, match_data: dict, puuid: str
    ) -> models.Model:
        data = self.get_match_participant_champion_stats_data(match_data, puuid)
        return self.update_or_create(**data)


class MatchParticipantChampionStats(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Match, on_delete=models.CASCADE, null=False)
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

    objects = MatchParticipantChampionStatsManager()
