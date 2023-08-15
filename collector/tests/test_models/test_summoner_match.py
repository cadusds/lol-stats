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
from ..generate_data import GenerateData
from django.test import TestCase
from unittest.mock import patch
from django.db.models.query import QuerySet


class SummonerMatchTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.lol_api = LeagueOfLegendsAPI()
        self.model = SummonerMatch
        self.puuid = "GLhL9HBmuajINZ9H2k-cBMvH0lU4ySKC4MkzX-u7K6qEqZMl3HS_wkdGvo-cXqhQ-Exm7gceXoGvOA"

    def mock_get_all_matchs_by_summoner_puuid(puuid):
        response = GenerateData.build_lol_api_matchs_response(True)
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
        "get_all_matchs_by_summoner_puuid",
        side_effect=mock_get_all_matchs_by_summoner_puuid,
    )
    @patch.object(
        LeagueOfLegendsAPI,
        "get_match_stats",
        return_value=GenerateData.build_lol_api_get_match_stats_method_response(),
    )
    def test_create_all_matchs_stats_by_puuid(
        self, mocked_stats, mocked_summoner_matchs
    ):
        summoner = SummonerFactory.create(puuid=self.puuid)
        summoner_matchs = SummonerMatch.objects.create_all_matchs_by_puuid(
            puuid=self.puuid
        )
        response = SummonerMatch.objects.create_all_matchs_stats_by_puuid(
            puuid=self.puuid
        )
        self.assertEqual(response, {"status": "ok"})
        self.assertEqual(len())
