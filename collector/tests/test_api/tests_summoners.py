import requests
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from collector.models import Summoner
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from collector.tests.generate_data import GenerateData
from collector.api.serializers import SummonerSerializer
from faker import Faker
from ..factories.summoner import SummonerFactory


fake = Faker()
fake_name = fake.name()


class SummonerAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.factory = APIRequestFactory()

    @patch.object(requests, "get", return_value=GenerateData.build_lol_api_summoner_response(fake_name))
    def test_create_summoner(self):
        url = reverse("summoner-list")
        response = self.client.post(url, {"name": fake_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Summoner.objects.count(), 1)
        summoner = Summoner.objects.first()
        self.assertEqual(summoner.name, fake_name)

    def test_create_summoner_already_exists(self):
        summoner_name = fake.name()
        SummonerFactory.create(name=summoner_name)
        url = reverse("summoner-list")
        response = self.client.post(url, {"name": summoner_name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = dict(error=f"The summoner {summoner_name} already exists.")
        self.assertEqual(response.data, expected_data)

    def test_retrieve_summoner(self):
        summoner = SummonerFactory.create(fake_name)
        response = self.client.get(
            reverse("summoner-detail", kwargs={"pk": summoner.pk})
        )
        summoner = SummonerSerializer(summoner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, summoner.data)

    def test_delete_summoner(self):
        summoner = SummonerFactory.create(fake_name)
        response = self.client.delete(
            reverse("summoner-detail", kwargs=dict(pk=summoner.pk))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Summoner.objects.count(), 0)

    def test_list_summoners(self):
        expected_response_data = list()
        for _ in range(5):
            summoner = SummonerSerializer(SummonerFactory.create(fake.name()))
            expected_response_data.append(summoner.data)
        self.assertEqual(Summoner.objects.count(), 5)
        response = self.client.get(reverse("summoner-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], expected_response_data)
