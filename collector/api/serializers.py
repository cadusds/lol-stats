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
        fields = ["summoner", "game"]


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Match
        fields = "__all__"
