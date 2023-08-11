from unittest.mock import patch
from django.test import TestCase
from collector.api.league_of_legends_api import LeagueOfLegendsAPI
from collector.tests.generate_data import GenerateData
from collector.models import MatchParticipantBasicStats
from ..factories.summoner import SummonerFactory
from ..factories.match import MatchFactory

class MatchParticipantBasicStatsTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.lol_api = LeagueOfLegendsAPI()
        self.model = MatchParticipantBasicStats
        self.puuid = "GLhL9HBmuajINZ9H2k-cBMvH0lU4ySKC4MkzX-u7K6qEqZMl3HS_wkdGvo-cXqhQ-Exm7gceXoGvOA"
    
    @patch.object(
        LeagueOfLegendsAPI,
        "get_match_stats",
        return_value=GenerateData.build_lol_api_get_match_stats_method_response(),
    )
    def test_get_match_participant_basic_stats_data(self,mocked):
        summoner = SummonerFactory.create(puuid=self.puuid)
        match_data = self.lol_api.get_match_stats("BR1_2000000000")
        MatchFactory.create(game_id=match_data['game_id'])
        _, created = self.model.objects.create_match_participant_basic_stats_object_with_match_data(match_data,summoner.puuid)
        self.assertTrue(created)