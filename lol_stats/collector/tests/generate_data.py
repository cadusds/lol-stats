import json
import uuid
import random
import string
import requests
import datetime


class GenerateData:
    
    def __init__(self) -> None:
        pass

    def get_random_string(length):
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
    
    def _build_summoner_response_data(self,summoner_name):
        return dict(
            id = str(uuid.uuid4()),
            accountId = str(uuid.uuid4()),
            puuid = str(uuid.uuid4()),
            name = summoner_name,
            profileIconId = str(uuid.uuid4()),
            revisionDate = datetime.datetime.utcnow().timestamp()*100,
            summonerLevel = random.randint(20,300)
        )
    
    def _build_match_response_data(self,last_response:bool=False):
        if last_response:
            return [ "BR1_" + str(random.randint(2000000000,3000000000)) for _ in range(100)]
        return [ "BR1_" + str(random.randint(2000000000,3000000000)) for _ in range(random.randint(1,99))]
        
    def build_lol_api_summoner_response(self,summoner_name):
        response = requests.Response()
        response._content = json.dumps(self._build_summoner_response_data(summoner_name)).encode('utf-8')
        return response
    
    def build_lol_api_matchs_response(self,last_response=False):
        data = self._build_match_response_data(last_response=last_response)
        response = requests.Response()
        response._content = json.dumps(data).encode('utf-8')
        return response
        
    