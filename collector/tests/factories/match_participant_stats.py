import factory
import factory.fuzzy
from collector import models
from .match import MatchFactory
from .summoner import SummonerFactory


class MatchParticipantStatsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MatchParticipantStats

    summoner = factory.SubFactory(SummonerFactory)
    game = factory.SubFactory(MatchFactory)
    champion_name = factory.Faker('name')
    total_damage_dealt = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    total_damage_dealt_to_champions = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    total_damage_taken = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    magic_damage_dealt = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    magic_damage_dealt_to_champions = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    magic_damage_taken = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    physical_damage_dealt = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    physical_damage_dealt_to_champions = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    physical_damage_taken = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    total_heal = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    total_minions_killed = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    total_time_spent_dead = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    true_damage_dealt = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    true_damage_dealt_to_champions = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    true_damage_taken = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    turrent_kills = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    turrent_takes = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    turrents_lost = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    vision_score = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    vision_wards_bought_in_game = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    wards_killed = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    wards_placed = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    gold_earned = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    gold_spent = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    longest_time_spent_living = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
    time_played = factory.fuzzy.FuzzyInteger(low=1000,high=10000)
