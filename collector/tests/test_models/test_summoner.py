import requests
from django.test import TestCase
from unittest.mock import patch
from collector.models import Summoner
from collector.tests.generate_data import GenerateData
from collector.api.league_of_legends_api import LeagueOfLegendsAPI
from faker import Faker
from ..factories.summoner import SummonerFactory


class SummonerTestCase(TestCase):
    def setUp(self) -> None:
        self.lol_api = LeagueOfLegendsAPI()
        self.factory = SummonerFactory

    @patch.object(
        requests,
        "get",
        return_value=GenerateData.build_lol_api_summoner_response("test"),
    )
    def test_create_summoner_by_name(self, mocked):
        summoner = Summoner.objects.create_summoner_by_name(name="test")
        requests.get.assert_called_with(
            f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/test",
            headers=self.lol_api.headers,
        )
        self.assertEqual(summoner.name, "test")
