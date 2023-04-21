import uuid
import datetime
from collector import models
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

class SummonersTestCase(TestCase):

    def setUp(self) -> None:
        models.Summoners.objects.create(
            summoner_id = uuid.uuid4(),
            account_id = uuid.uuid4(),
            puuid = uuid.uuid4(),
            name = "TestSummoner",
            profile_icon_id = uuid.uuid4(),
            revision_date = datetime.datetime(2022,1,1),
            summoner_level = 101
        )
    
    def test_create_info(self):
        summoner = models.Summoners.objects.get(name="TestSummoner")
        self.assertEqual(summoner.name,"TestSummoner")
        self.assertEqual(summoner.revision_date, datetime.datetime(2022,1,1,tzinfo=datetime.timezone.utc))
        self.assertEqual(summoner.summoner_level,101)

class SummonersAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.summoner_data = dict(
            summoner_id = uuid.uuid4(),
            account_id = uuid.uuid4(),
            puuid = uuid.uuid4(),
            name = "TestSummoner",
            profile_icon_id = uuid.uuid4(),
            revision_date = datetime.datetime(2022,1,1),
            summoner_level = 101
        )

    def test_create_summoner(self):
        url = reverse("summoner-list")
        response = self.client.post(url,self.data,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Summoners.objects.count(),1)
        self.assertEqual(models.Summoners.objects.get().name,"TestSummoner")
    
    def test_retrieve_summoner(self):
        summoner = models.Summoners.objects.create(**self.summoner_data)
        response = self.client.get(reverse('summoner-retrieve',kwargs={"pk":summoner.pk}))
        self.assertEqual(response.data,self.summoner_data)