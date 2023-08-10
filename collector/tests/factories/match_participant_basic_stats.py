import factory
import factory.fuzzy
from collector import models
from collector.tests.generate_data import GenerateData


class MatchParticipantBasicStatsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MatchParticipantBasicStats

    # summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, null=False)
    # game_id = models.ForeignKey(SummonerMatch, on_delete=models.CASCADE, null=False)
    # team_position = models.CharField(max_length=200)
    # deaths = models.IntegerField()
    # assists = models.IntegerField()
    # kills = models.IntegerField()
    # double_kills = models.IntegerField()
    # triple_kills = models.IntegerField()
    # quadra_kills = models.IntegerField()
    # penta_kills = models.IntegerField()
    # first_blood_kill = models.BooleanField()
    # first_blood_assist = models.BooleanField()
    # first_tower_kill = models.BooleanField()
    # first_tower_assist = models.BooleanField()
    # largest_multi_kill = models.IntegerField()
    # win = models.BooleanField()
