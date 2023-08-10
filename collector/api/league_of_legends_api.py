import os
import requests
import datetime
import dotenv

dotenv.load_dotenv()


class LeagueOfLegendsAPI:
    BASE_ENDPOINT = "https://{route}.api.riotgames.com/lol/"
    API_KEY = os.environ.get("LOL_API_TOKEN")

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": "RGAPI-982bd379-3931-4dae-9483-88fa1c696057",
        }

    def get_summoner(self, summoner_name: str) -> dict:
        endpoint = (
            self.BASE_ENDPOINT.format(route="br1")
            + f"summoner/v4/summoners/by-name/{summoner_name}"
        )
        rename_keys = {
            "id": "summoner_id",
            "accountId": "account_id",
            "puuid": "puuid",
            "name": "name",
            "profileIconId": "profile_icon_id",
            "revisionDate": "revision_date",
            "summonerLevel": "summoner_level",
        }
        response = requests.get(endpoint, headers=self.headers)
        if not response.ok:
            raise Exception(response.status_code)
        else:
            response = response.json()
        summonner_data = {rename_keys[k]: v for k, v in response.items()}
        revision_date = datetime.datetime.fromtimestamp(
            summonner_data["revision_date"] / 100
        )
        summonner_data["revision_date"] = revision_date
        return summonner_data

    def get_all_matchs_by_summoner_puuid(self, puuid):
        endpoint = (
            self.BASE_ENDPOINT.format(route="americas")
            + f"match/v5/matches/by-puuid/{puuid}/ids"
        )
        init_date = datetime.datetime(2021, 6, 16).timestamp()
        data = {"count": 100, "start": 0, "startTime": int(init_date)}
        response = list()
        while True:
            matchs = requests.get(endpoint, params=data, headers=self.headers).json()
            response += matchs
            if len(matchs) < 100:
                break
            data["start"] += 100
        return [{"summoner": puuid, "match_id": match_id} for match_id in response]

    def get_match_stats(self, match_id) -> dict:
        endpoint = (
            self.BASE_ENDPOINT.format(route="americas") + f"match/v5/matches/{match_id}"
        )
        response = requests.get(endpoint, headers=self.headers)
        match response.ok:
            case True:
                return response.json()
            case False:
                raise Exception(f"Request Error\nstatus_code:{response.status_code}")
