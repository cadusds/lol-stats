import json
import uuid
import random
import string
import requests
import datetime


class GenerateData:
    @classmethod
    def get_random_string(cls, length):
        letters = string.ascii_letters
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str

    @classmethod
    def _build_summoner_response_data(cls, summoner_name):
        return dict(
            id=str(uuid.uuid4()),
            accountId=str(uuid.uuid4()),
            puuid=str(uuid.uuid4()),
            name=summoner_name,
            profileIconId=str(uuid.uuid4()),
            revisionDate=datetime.datetime.utcnow().timestamp() * 100,
            summonerLevel=random.randint(20, 300),
        )

    @classmethod
    def _build_match_response_data(cls, last_response: bool = False):
        if last_response:
            return ["BR1_" + str(x) for x in range(2000000000, 2000000100)]
        return ["BR1_" + str(x) for x in range(2000000000, 2000000099)]

    @classmethod
    def build_lol_api_summoner_response(cls, summoner_name):
        response = requests.Response()
        response._content = json.dumps(
            cls._build_summoner_response_data(summoner_name)
        ).encode("utf-8")
        response.status_code = 200
        return response

    @classmethod
    def build_lol_api_matchs_response(cls, last_response=False):
        data = cls._build_match_response_data(last_response=last_response)
        response = requests.Response()
        response._content = json.dumps(data).encode("utf-8")
        return response
