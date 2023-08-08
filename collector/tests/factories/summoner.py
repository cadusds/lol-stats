from factory.django import DjangoModelFactory
from collector.tests.generate_data import GenerateData

class SummonerFactory(DjangoModelFactory):
    class Meta:
        model = 'collector.Summoner'
        django_get_or_create = ('name',)
    
    name = 'Summoner ' + GenerateData.get_random_string(6)