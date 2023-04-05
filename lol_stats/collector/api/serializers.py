from collector import models
from rest_framework import serializers


class SummonersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Summoners
        fields = ['summoner_id', 'account_id', 'name', 'profile_icon_id', 'revision_date', 'summoner_level']