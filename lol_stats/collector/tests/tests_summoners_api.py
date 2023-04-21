import uuid
import datetime
from collector.models import Summoners
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from collector.api.serializers import SummonersSerializer


class SummonersAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.summoner_data = self.build_summoner_data()
    
    def build_summoner_data(self):
        return dict(
            summoner_id = str(uuid.uuid4()),
            account_id = str(uuid.uuid4()),
            puuid = uuid.uuid4(),
            name = "TestSummoner",
            profile_icon_id = uuid.uuid4(),
            revision_date = datetime.datetime(2022,1,1),
            summoner_level = 101
        )

    def create_summoner(self):
        data = self.build_summoner_data()
        return Summoners.objects.create(**data)

    def test_create_summoner(self):
        url = reverse("summoner-list")
        response = self.client.post(url,self.summoner_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Summoners.objects.count(),1)
        self.assertEqual(Summoners.objects.get().name,"TestSummoner")
    
    def test_retrieve_summoner(self):
        summoner = Summoners.objects.create(**self.summoner_data)
        response = self.client.get(reverse('summoner-detail',kwargs={"pk":summoner.pk}))
        summoner = SummonersSerializer(summoner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,summoner.data)
    
    def test_delete_summoner(self):
        summoner = Summoners.objects.create(**self.summoner_data)
        response = self.client.delete(reverse('summoner-detail',kwargs=dict(pk=summoner.pk)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Summoners.objects.count(),0)
    
    def test_list_summoners(self):
        expected_response_data = list()
        for _ in range(5):
            summoner = SummonersSerializer(self.create_summoner())
            expected_response_data.append(summoner.data)
        self.assertEqual(Summoners.objects.count(),5)
        response = self.client.get(reverse('summoner-list'),format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'],expected_response_data)
            
        