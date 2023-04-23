import uuid
import json
import requests
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from unittest.mock import MagicMock
from collector.models import Summoner
from rest_framework.test import APITestCase
from collector.api.serializers import SummonerSerializer
from collector.api.league_of_legends_api import LeagueOfLegendsAPI


def build_summoner_data():
    return dict(
        id = str(uuid.uuid4()),
        accountId = str(uuid.uuid4()),
        puuid = str(uuid.uuid4()),
        name = "xxxx",
        profileIconId = str(uuid.uuid4()),
        revisionDate = 1682179506000,
        summonerLevel = 101
    )

def build_summoner_response():
    response = requests.Response()
    response._content = json.dumps(build_summoner_data()).encode('utf-8')
    return response

class SummonerTestCase(TestCase):

    def setUp(self) -> None:
        self.lol_api = LeagueOfLegendsAPI()
    
    def test_create_summoner(self):
        requests.get = MagicMock()
        requests.get.return_value = build_summoner_response()
        summoner = Summoner.objects.create("xxxx")
        requests.get.assert_called_with("https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/xxxx", headers=self.lol_api.headers)
        self.assertEqual(summoner.name, "xxxx")

class SummonerAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def create_summoner(self):
        requests.get = MagicMock()
        requests.get.return_value = build_summoner_response()
        return Summoner.objects.create("xxxx")

    def test_create_summoner(self):
        url = reverse("summoner-list")
        response = self.client.post(url,{"name":"xxxx"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Summoner.objects.count(),1)
        summoner = Summoner.objects.first()
        self.assertEqual(summoner.name,"xxxx")
    
    def test_retrieve_summoner(self):
        summoner = Summoner.objects.create("xxxx")
        response = self.client.get(reverse('summoner-detail',kwargs={"pk":summoner.pk}))
        summoner = SummonerSerializer(summoner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,summoner.data)
    
    def test_delete_summoner(self):
        summoner = Summoner.objects.create("xxxx")
        response = self.client.delete(reverse('summoner-detail',kwargs=dict(pk=summoner.pk)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Summoner.objects.count(),0)
    
    def test_list_summoners(self):
        expected_response_data = list()
        for _ in range(5):
            summoner = SummonerSerializer(self.create_summoner())
            expected_response_data.append(summoner.data)
        self.assertEqual(Summoner.objects.count(),5)
        response = self.client.get(reverse('summoner-list'),format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'],expected_response_data)
            
        