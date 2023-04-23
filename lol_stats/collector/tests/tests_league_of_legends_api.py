import uuid
import json
import requests
import datetime
from django.test import TestCase
from unittest.mock import MagicMock
from collector.api.league_of_legends_api import LeagueOfLegendsAPI



class LeagueOfLegendsAPITestCase(TestCase):

    def setUp(self) -> None:
        self.lol_api = LeagueOfLegendsAPI()
        self.summonner_data = self.build_summoner_data()
    
    def build_summoner_data(self):
        return dict(
            id = str(uuid.uuid4()),
            accountId = str(uuid.uuid4()),
            puuid = str(uuid.uuid4()),
            name = "xxxx",
            profileIconId = str(uuid.uuid4()),
            revisionDate = datetime.datetime.timestamp(datetime.datetime.utcnow())*100,
            summonerLevel = 101
        )
    
    def build_summoner_response(self):
        response = requests.Response()
        response._content = json.dumps(self.summonner_data).encode('utf-8')
        return response
    
    def test_get_summoner(self):
        requests.get = MagicMock()
        requests.get.return_value = self.build_summoner_response()
        response = self.lol_api.get_summoner("xxxx")
        self.assertIsInstance(response,dict)
        requests.get.assert_called_with("https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/xxxx", headers=self.lol_api.headers)
        self.assertEqual(response["revision_date"],datetime.datetime.fromtimestamp(self.summonner_data["revisionDate"]/100))