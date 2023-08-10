import factory
import factory.fuzzy
from collector import models
from collector.tests.generate_data import GenerateData
from .summoner import SummonerFactory
from .match import MatchFactory


class MatchParticipantBasicStatsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MatchParticipantBasicStats

    summoner = factory.SubFactory(SummonerFactory)
    game = factory.SubFactory(MatchFactory)
    team_position = factory.fuzzy.FuzzyText(length=10)
    deaths = factory.fuzzy.FuzzyInteger(low=0,high=15)
    assists = factory.fuzzy.FuzzyInteger(low=0,high=15)
    kills = factory.fuzzy.FuzzyInteger(low=0,high=15)
    double_kills = factory.fuzzy.FuzzyInteger(low=0,high=10)
    triple_kills = factory.fuzzy.FuzzyInteger(low=0,high=6)
    quadra_kills = factory.fuzzy.FuzzyInteger(low=0,high=3)
    penta_kills = factory.fuzzy.FuzzyInteger(low=0,high=2)
    first_blood_kill = factory.fuzzy.FuzzyChoice([True,False])
    first_blood_assist = factory.fuzzy.FuzzyChoice([True,False])
    first_tower_kill = factory.fuzzy.FuzzyChoice([True,False])
    first_tower_assist = factory.fuzzy.FuzzyChoice([True,False])
    largest_multi_kill = factory.fuzzy.FuzzyInteger(low=0,high=10)
    win = factory.fuzzy.FuzzyChoice([True,False])
