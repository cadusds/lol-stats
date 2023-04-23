import requests
from django.test import TestCase
from unittest.mock import MagicMock
from collector.api.league_of_legends_api import LeagueOfLegendsAPI


class LeagueOfLegendsAPITestCase(TestCase):

    def setUp(self) -> None:
        self.lol_api = LeagueOfLegendsAPI()
    
    def build_summoner_response(self):
        response = requests.Response()
        response._content = """{
            "id": "xxx-xxx",
            "accountId": "xxxxx",
            "puuid": "xxx-xxx",
            "name": "xxxx",
            "profileIconId": 4378,
            "revisionDate": 1682179506000,
            "summonerLevel": 116
        }""".encode('utf-8')
        return response
    
    def test_get_summoner(self):
        requests.get = MagicMock()
        requests.get.return_value = self.build_summoner_response()
        response = self.lol_api.get_summoner("xxxx")
        self.assertIsInstance(response,dict)
        requests.get.assert_called_with("https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/xxxx", headers=self.lol_api.headers)