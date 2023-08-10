import factory
import random
from collector import models
from .summoner import SummonerFactory
from collector.tests.generate_data import GenerateData


def generate_match_id() -> str:
    options = GenerateData._build_match_response_data()
    return random.choice(options)


class SummonerMatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SummonerMatch

    summoner = factory.SubFactory(SummonerFactory)
    match_id = factory.LazyFunction(generate_match_id)
    game_id = factory.LazyAttribute(lambda x: x.match_id.replace("BR1_", ""))
