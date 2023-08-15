import factory
import factory.fuzzy
from collector import models
from .summoner import SummonerFactory
from .match import MatchFactory


class MatchParticipantChampionStatsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MatchParticipantChampionStats
    
    summoner = factory.SubFactory(SummonerFactory)
    game = factory.SubFactory(MatchFactory)
    champion_name = factory.Faker("name")
    champ_experience = factory.fuzzy.FuzzyInteger(low=0, high=1800)
    champ_level = factory.fuzzy.FuzzyInteger(low=0, high=18)
    items_purchased = factory.fuzzy.FuzzyInteger(low=0, high=6)
    item0 = factory.fuzzy.FuzzyInteger(low=0, high=15)
    item1 = factory.fuzzy.FuzzyInteger(low=0, high=15)
    item2 = factory.fuzzy.FuzzyInteger(low=0, high=15)
    item3 = factory.fuzzy.FuzzyInteger(low=0, high=15)
    item4 = factory.fuzzy.FuzzyInteger(low=0, high=15)
    item5 = factory.fuzzy.FuzzyInteger(low=0, high=15)
    item6 = factory.fuzzy.FuzzyInteger(low=0, high=15)
    spell1_casts = factory.fuzzy.FuzzyInteger(low=0, high=150)
    spell2_casts = factory.fuzzy.FuzzyInteger(low=0, high=150)
    spell3_casts = factory.fuzzy.FuzzyInteger(low=0, high=150)
    spell4_casts = factory.fuzzy.FuzzyInteger(low=0, high=50)
