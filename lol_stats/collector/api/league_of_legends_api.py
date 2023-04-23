import os
import requests


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
        return requests.get(endpoint,headers=self.headers).json()