import requests
from unittest.mock import patch
from django.test import TestCase
from collector.models import Match
from collector.api.league_of_legends_api import LeagueOfLegendsAPI
from collector.tests.generate_data import GenerateData


class MatchTestCase(TestCase):
    @patch.object(
        LeagueOfLegendsAPI,
        "get_match_stats",
        return_value=GenerateData.build_lol_api_get_match_stats_method_response(),
    )
    def test_create_match_object_with_match_data(self, mocked):
        match_data = LeagueOfLegendsAPI().get_match_stats("BR1_2000000000")
        _, created = Match.objects.create_match_object_with_match_data(match_data)
        self.assertTrue(created)
        self.assertEqual(Match.objects.all().count(), 1)

    @patch.object(
        LeagueOfLegendsAPI,
        "get_match_stats",
        return_value=GenerateData.build_lol_api_get_match_stats_method_response(),
    )
    def test_get_match_stats_data(self, mocked):
        match_data = LeagueOfLegendsAPI().get_match_stats("BR1_2000000000")
        response = Match.objects.get_match_stats_data(match_data)
        self.assertIsInstance(response, dict)
        self.assertEqual(
            list(response.keys()),
            [
                "game_id",
                "game_creation",
                "game_start_timestamp",
                "game_end_timestamp",
                "game_duration",
                "game_mode",
                "game_name",
                "game_type",
                "game_version",
                "map_id",
                "platform_id",
                "queue_id",
                "teams",
                "tournament_code",
            ],
        )
