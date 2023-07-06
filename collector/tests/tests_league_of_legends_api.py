import uuid
import random
import requests
import datetime
from django.test import TestCase
from unittest.mock import MagicMock, patch
from collector.api.league_of_legends_api import LeagueOfLegendsAPI
from collector.tests.generate_data import GenerateData


class LeagueOfLegendsAPITestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.lol_api = LeagueOfLegendsAPI()
        self.summonner_data = GenerateData._build_summoner_response_data(
            GenerateData.get_random_string(10)
        )

    @patch.object(
        requests,
        "get",
        return_value=GenerateData.build_lol_api_summoner_response("test"),
    )
    def test_get_summoner(self, mocked):
        response = self.lol_api.get_summoner(mocked.json()["name"])
        self.assertIsInstance(response, dict)
        requests.get.assert_called_with(
            f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{mocked.json()['name']}",
            headers=self.lol_api.headers,
        )
        self.assertEqual(
            response["revision_date"],
            datetime.datetime.fromtimestamp(
                mocked.return_value.json()["revisionDate"] / 100
            ),
        )

    def mock_response_error():
        class MockResponseError:
            def __init__(self) -> None:
                self.ok = False
                self.status_code = 400

            def json(self):
                return {}

        return MockResponseError()

    @patch.object(requests, "get", return_value=mock_response_error())
    def test_get_summoner_error(self, mocked):
        with self.assertRaises(Exception) as cmd:
            self.lol_api.get_summoner("test")
        mocked.assert_called()
        self.assertEqual(str(cmd.exception), "400")

    def mock_response_to_get_matchs():
        response = GenerateData.build_lol_api_matchs_response
        return [response(True), response()]

    def test_fail(self):
        self.assertEqual(1, 2)

    @patch.object(requests, "get", side_effect=mock_response_to_get_matchs())
    def test_get_all_matchs_by_summoner_puuid_with_more_than_one_responses(
        self, mocked
    ):
        puuid = str(uuid.uuid4())
        response = self.lol_api.get_all_matchs_by_summoner_puuid(puuid)
        self.assertIsInstance(response, list)
        list_match_ids = self.list_all_matchs_ids(
            [
                GenerateData.build_lol_api_matchs_response(True),
                GenerateData.build_lol_api_matchs_response(),
            ]
        )
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
        responses = [x.json() for x in responses]
        matchs_ids = list()
        for response in responses:
            matchs_ids += response
        return matchs_ids

    def order_list_by_match_id(self, dct):
        return dct["match_id"]
