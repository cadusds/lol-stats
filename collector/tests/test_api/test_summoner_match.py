from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from ..generate_data import GenerateData
from rest_framework.test import APITestCase
from ..factories.summoner import SummonerFactory
from collector.models import Summoner, SummonerMatch
from collector.api.league_of_legends_api import LeagueOfLegendsAPI


class SummonerMatchAPITestCase(APITestCase):
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
    def test_create(self, mocked):
        summoner_name = "SummonerTest"
        SummonerFactory.create(name=summoner_name)
        url = reverse("summoner_match-list")
        response = self.client.post(url, data={"name": summoner_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SummonerMatch.objects.count(), 100)

    def test_create_when_summoner_not_exists(self):
        url = reverse("summoner_match-list")
        response = self.client.post(url, data={"name": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"error": "The summoner with name test, not exists"}
        )
