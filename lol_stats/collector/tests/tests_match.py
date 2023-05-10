import requests
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from unittest.mock import MagicMock
from rest_framework.test import APITestCase
from collector.models import Match, Summoner
from collector.tests.generate_data import GenerateData




class MatchTestCase(TestCase):
    
    def setUp(self) -> None:
        self.maxDiff = None
        requests.get = MagicMock()
        requests.get.return_value = GenerateData().build_lol_api_summoner_response("SummonerTest")
        self.summoner = Summoner.objects.create("SummonerTest")
    
    def test_create_all_matchs_by_puuid(self):
        matchs = Match.objects.create_all_matchs_by_puuid(puuid=self.summoner.puuid)
        self.assertIsInstance(matchs,list)
        for match in matchs:
            self.assertEqual(str(match.puuid.pk),self.summoner.pk)

class MatchAPITestCase(APITestCase):
    
    def setUp(self) -> None:
        self.maxDiff = None
        requests.get = MagicMock()
        requests.get.return_value = GenerateData().build_lol_api_summoner_response("SummonerTest")
        self.summoner = Summoner.objects.create("SummonerTest")
    
    def test_create(self):
        url = reverse("match-list")
        requests.post = MagicMock()
        mock_response = GenerateData().build_lol_api_matchs_response
        mock_responses = [mock_response(True),mock_response()]
        requests.post.side_effect = mock_responses
        response = self.client.post(url,data={"name":"SummonerTest"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(),7)
