import uuid
import random
import requests
import datetime
from django.test import TestCase
from unittest.mock import MagicMock, patch
from collector.api.league_of_legends_api import LeagueOfLegendsAPI
from collector.tests.generate_data import GenerateData


class LeagueOfLegendsAPITestCase(TestCase):
    class MockResponseError:
        def __init__(self) -> None:
            self.ok = False
            self.status_code = 400

        def json(self):
            return {}

    def setUp(self) -> None:
        self.maxDiff = None
        self.lol_api = LeagueOfLegendsAPI()
        self.summonner_data = GenerateData()._build_summoner_response_data(
            GenerateData.get_random_string(10)
        )

    def test_get_summoner(self):
        requests.get = MagicMock()
        mock_response = GenerateData().build_lol_api_summoner_response(
            GenerateData.get_random_string(10)
        )
        requests.get.return_value = mock_response
        response = self.lol_api.get_summoner(mock_response.json()["name"])
        self.assertIsInstance(response, dict)
        requests.get.assert_called_with(
            f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{mock_response.json()['name']}",
            headers=self.lol_api.headers,
        )
        self.assertEqual(
            response["revision_date"],
            datetime.datetime.fromtimestamp(mock_response.json()["revisionDate"] / 100),
        )

    @patch.object(requests, "get", return_value=MockResponseError())
    def test_get_summoner_error(self, mocked):
        with self.assertRaises(Exception) as cmd:
            self.lol_api.get_summoner("test")
        mocked.assert_called()
        self.assertEqual(str(cmd.exception), "400")

    def test_get_all_matchs_by_summoner_puuid_with_more_than_one_responses(self):
        requests.get = MagicMock()
        mock_response = GenerateData().build_lol_api_matchs_response
        mock_responses = [mock_response(True), mock_response()]
        requests.get.side_effect = mock_responses
        puuid = str(uuid.uuid4())
        response = self.lol_api.get_all_matchs_by_summoner_puuid(puuid)
        self.assertIsInstance(response, list)
        list_match_ids = self.list_all_matchs_ids(mock_responses)
        expected_response = [{"puuid": puuid, "match_id": x} for x in list_match_ids]
        self.assertEqual(len(response), len(expected_response))
        self.assertEqual(requests.get.call_count, 2)
        start_time = requests.get.call_args[1]["params"]["startTime"]
        requests.get.assert_called_with(
            f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids",
            params={"count": 100, "start": 100, "startTime": start_time},
            headers=self.lol_api.headers,
        )

    def list_all_matchs_ids(self, responses: list):
        matchs_ids = list()
        for response in responses:
            matchs_ids += response.json()
        return matchs_ids

    def order_list_by_match_id(self, dct):
        return dct["match_id"]
