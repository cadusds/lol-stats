import factory
import factory.fuzzy
import random
from collector import models
from .summoner import SummonerFactory
from collector.tests.generate_data import GenerateData


class SummonerMatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SummonerMatch

    summoner = factory.SubFactory(SummonerFactory)
    match_id = factory.fuzzy.FuzzyChoice(GenerateData._build_match_response_data())
    game_id = factory.LazyAttribute(lambda x: x.match_id.replace("BR1_", ""))
