from django.test import TestCase
from unittest.mock import patch
from ..factories.summoner import SummonerFactory

class SummonerMatchTestCase(TestCase):

    def setUp(self) -> None:
        pass

    def test_create_all_matchs_by_puuid(self):
        summoner = SummonerFactory.create(name='test')
        self.assertEqual(summoner.name,"test")

