import factory
from collector import models

class SummonerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Summoner
    
    name = factory.Faker('name')