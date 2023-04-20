import uuid
import datetime
from django.test import TestCase
from collector import models


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
