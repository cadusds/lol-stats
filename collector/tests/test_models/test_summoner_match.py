from django.test import TestCase
from unittest.mock import patch
from ..factories.summoner import SummonerFactory
from ..generate_data import GenerateData
from collector.models import Summoner, SummonerMatch
from collector.api.league_of_legends_api import LeagueOfLegendsAPI


class SummonerMatchTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

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
        self.assertIsInstance(matchs, list)
        for match in matchs:
            self.assertEqual(str(match.summoner.pk), summoner_test.pk)
            self.assertIn("BR1", match.match_id)
            self.assertIsInstance(match.game_id, str)
