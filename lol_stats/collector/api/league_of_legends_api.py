import os
import requests
import datetime

class LeagueOfLegendsAPI:

    BASE_ENDPOINT = "https://{route}.api.riotgames.com/lol/"
    API_KEY = os.environ.get("LOL_API_TOKEN")

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.API_KEY
        }
    
    def get_summoner(self, summoner_name:str) -> dict:
        endpoint = self.BASE_ENDPOINT.format(route="br1") + f"summoner/v4/summoners/by-name/{summoner_name}"
        rename_keys = {
            "id": "summoner_id",
            "accountId": "account_id",
            "puuid": "puuid",
            "name": "name",
            "profileIconId": "profile_icon_id",
            "revisionDate": "revision_date",
            "summonerLevel": "summoner_level" 
        }
        response = requests.get(endpoint,headers=self.headers).json()
        summonner_data = {rename_keys[k]:v for k,v in response.items()}
        revision_date = datetime.datetime.fromtimestamp(summonner_data["revision_date"]/100)
        summonner_data["revision_date"] = revision_date
        return summonner_data

    def get_all_matchs_by_summoner_puuid(self,puuid):
        endpoint = self.BASE_ENDPOINT.format(route="americas") + f"match/v5/matches/by-puuid/{puuid}/ids"
        data = dict(count=100,start=0)
        response = requests.get(endpoint,data=data,headers=self.headers).json()
        while len(response) == 100:
            data["start"] =+ 100
            matchs = requests.get(endpoint,data=data,headers=self.headers).json()
            response += matchs
        return [{"puuid":puuid, "match_id": match_id} for match_id in response]
