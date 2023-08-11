import factory
import factory.fuzzy
from collector import models
from collector.tests.generate_data import GenerateData


def generate_game_id() -> str:
    match_id_list = GenerateData._build_match_response_data()
    return [x.replace("BR_", "") for x in match_id_list]


class MatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Match

    game_id = factory.fuzzy.FuzzyChoice(generate_game_id)
    game_creation = factory.fuzzy.FuzzyText(length=10)
    game_start_timestamp = factory.fuzzy.FuzzyText(length=10)
    game_end_timestamp = factory.fuzzy.FuzzyText(length=10)
    game_duration = factory.fuzzy.FuzzyText(length=10)
    game_mode = factory.fuzzy.FuzzyText(length=10)
    game_name = factory.fuzzy.FuzzyText(length=10)
    game_type = factory.fuzzy.FuzzyText(length=10)
    game_version = factory.fuzzy.FuzzyText(length=10)
    map_id = factory.fuzzy.FuzzyInteger(low=2000,high=3000)
    platform_id = factory.fuzzy.FuzzyText(length=10)
    queue_id = factory.fuzzy.FuzzyInteger(low=2000,high=3000)
    teams = {}
    tournament_code = factory.fuzzy.FuzzyText(length=10)
