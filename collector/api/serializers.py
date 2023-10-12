from collector import models
from rest_framework import serializers


class SummonerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Summoner
        fields = [
            "puuid",
            "summoner_id",
            "account_id",
            "name",
            "profile_icon_id",
            "revision_date",
            "summoner_level",
        ]


class SummonerMatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SummonerMatch
        fields = ["summoner", "game", "match_id"]


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Match
        fields = "__all__"


class MatchParticipantBasicStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MatchParticipantBasicStats
        fields = [
            "summoner",
            "game",
            "team_position",
            "deaths",
            "assists",
            "kills",
            "double_kills",
            "triple_kills",
            "quadra_kills",
            "penta_kills",
            "first_blood_kill",
            "first_blood_assist",
            "first_tower_kill",
            "first_tower_assist",
            "largest_multi_kill",
            "win",
        ]


class MatchParticipantStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MatchParticipantStats
        fields = [
            "summoner",
            "game",
            "champion_name",
            "total_damage_dealt",
            "total_damage_dealt_to_champions",
            "total_damage_taken",
            "magic_damage_dealt",
            "magic_damage_dealt_to_champions",
            "magic_damage_taken",
            "physical_damage_dealt",
            "physical_damage_dealt_to_champions",
            "physical_damage_taken",
            "total_heal",
            "total_minions_killed",
            "total_time_spent_dead",
            "true_damage_dealt",
            "true_damage_dealt_to_champions",
            "true_damage_taken",
            "turret_kills",
            "turret_takedowns",
            "turrets_lost",
            "vision_score",
            "vision_wards_bought_in_game",
            "wards_killed",
            "wards_placed",
            "gold_earned",
            "gold_spent",
            "longest_time_spent_living",
            "time_played",
        ]


class MatchParticipantsChampionStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MatchParticipantChampionStats
        fields = [
            "summoner",
            "game",
            "champion_name",
            "champ_experience",
            "champ_level",
            "items_purchased",
            "item0",
            "item1",
            "item2",
            "item3",
            "item4",
            "item5",
            "item6",
            "spell1_casts",
            "spell2_casts",
            "spell3_casts",
            "spell4_casts",
        ]
