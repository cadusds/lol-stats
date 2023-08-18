from collector.api.league_of_legends_api import LeagueOfLegendsAPI
from collector.models import (
    Summoner,
    SummonerMatch,
    Match,
    MatchParticipantBasicStats,
    MatchParticipantChampionStats,
    MatchParticipantStats,
)
from ..factories.summoner import SummonerFactory
from ..factories.match import MatchFactory
from ..factories.summoner_match import SummonerMatchFactory
from ..generate_data import GenerateData
from django.test import TestCase
from unittest.mock import patch
from django.db.models.query import QuerySet
import factory

class SummonerMatchTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.lol_api = LeagueOfLegendsAPI()
        self.model = SummonerMatch
        self.puuid = "GLhL9HBmuajINZ9H2k-cBMvH0lU4ySKC4MkzX-u7K6qEqZMl3HS_wkdGvo-cXqhQ-Exm7gceXoGvOA"

    def mock_get_all_matchs_by_summoner_puuid(puuid):
        response = GenerateData.build_lol_api_matchs_response(True,10)
        summoner = Summoner.objects.filter(puuid=puuid)
        return [
            {"summoner": summoner, "match_id": match_id} for match_id in response.json()
        ]

    @patch.object(
        LeagueOfLegendsAPI,
        "get_all_matchs_by_summoner_puuid",
        side_effect=mock_get_all_matchs_by_summoner_puuid,
    )
    def test_create_all_matchs_by_puuid(self, mocked):
        summoner_test = SummonerFactory.create(name="test")
        matchs = SummonerMatch.objects.create_all_matchs_by_puuid(
            puuid=summoner_test.puuid
        )
        self.assertIsInstance(matchs, QuerySet)
        for match in matchs:
            self.assertEqual(str(match.summoner.pk), summoner_test.pk)
            self.assertIn("BR1", match.match_id)
            self.assertIsInstance(match.game_id, str)

    @patch.object(
        LeagueOfLegendsAPI,
        "get_match_stats",
        side_effect=GenerateData.build_lol_api_get_match_stats_method_response,
    )
    def test_create_all_matchs_stats_by_puuid(self,mocked):
        summoner = SummonerFactory.create(puuid=self.puuid)
        matchs = MatchFactory.create_batch(5,game_id=factory.Sequence(lambda x: f"2000000{x}"))
        for game in matchs:
            SummonerMatchFactory.create(game_id=game.game_id,summoner=summoner)
        response = SummonerMatch.objects.create_all_matchs_stats_by_puuid(puuid=summoner.puuid)
        self.assertEqual(response,{"status":"ok"})
        self.assertEqual(SummonerMatch.objects.count(),5)
        self.assertEqual(MatchParticipantBasicStats.objects.count(),5)
        self.assertEqual(MatchParticipantChampionStats.objects.count(),5)
        self.assertEqual(MatchParticipantStats.objects.count(),5)