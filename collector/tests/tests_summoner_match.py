import requests
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from unittest.mock import MagicMock, patch
from rest_framework.test import APITestCase
from django.db.models.query import QuerySet
from collector.models import SummonerMatch, Summoner, Match
from collector.tests.generate_data import GenerateData
from collector.api.league_of_legends_api import LeagueOfLegendsAPI


class SummonerMatchTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        requests.get = MagicMock()
        requests.get.return_value = GenerateData.build_lol_api_summoner_response(
            "SummonerTest"
        )
        self.summoner = Summoner.objects.create("SummonerTest")

    def mock_get_all_matchs_by_summoner_puuid(puuid):
        response = GenerateData.build_lol_api_matchs_response(True)
        summoner = Summoner.objects.get(puuid=puuid)
        return [
            {"summoner": summoner, "match_id": match_id} for match_id in response.json()
        ]

    @patch.object(
        LeagueOfLegendsAPI,
        "get_all_matchs_by_summoner_puuid",
        side_effect=mock_get_all_matchs_by_summoner_puuid,
    )
    def test_create_all_matchs_by_puuid(self, mocked):
        matchs = SummonerMatch.objects.create_all_matchs_by_puuid(
            puuid=self.summoner.puuid
        )
        self.assertIsInstance(matchs, QuerySet)
        for match in matchs:
            self.assertEqual(str(match.summoner.pk), self.summoner.pk)
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
    def test_create_all_matchs_stats_by_puuid(self, mocked_match_stats, mocked_matchs):
        SummonerMatch.objects.create_all_matchs_by_puuid(puuid=self.summoner.puuid)
        self.assertEqual(
            SummonerMatch.objects.filter(summoner=self.summoner).count(), 100
        )
        results = SummonerMatch.objects.create_all_matchs_stats_by_puuid(self.summoner.puuid)
        # self.assertEqual(Match.objects.all().count(), 100)
        self.assertEqual(results,[])


class SummonerMatchAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        requests.get = MagicMock()
        requests.get.return_value = GenerateData.build_lol_api_summoner_response(
            "SummonerTest"
        )
        self.summoner = Summoner.objects.create("SummonerTest")

    def mount_matchs_responses():
        return [
            GenerateData.build_lol_api_matchs_response(True),
            GenerateData.build_lol_api_matchs_response(),
        ]

    @patch.object(requests, "post", side_efect=mount_matchs_responses())
    def test_create(self, mocked):
        url = reverse("match-list")
        response = self.client.post(url, data={"name": "SummonerTest"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SummonerMatch.objects.count(), 7)

    @patch.object(
        requests,
        "post",
        return_value=GenerateData.build_lol_api_matchs_response(True),
    )
    def test_create_with_invalid_summoner(self, mocked):
        url = reverse("match-list")
        self.client.post(url, data={"name": "test"})
