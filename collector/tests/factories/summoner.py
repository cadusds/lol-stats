import factory,datetime
from collector import models
from ..generate_data import GenerateData



def generate_random_string():
    return GenerateData.get_random_string(20)
class SummonerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Summoner
    
    puuid = factory.LazyFunction(generate_random_string)
    summoner_id = factory.LazyFunction(generate_random_string)
    account_id = factory.LazyFunction(generate_random_string)
    name = factory.Faker('first_name')
    profile_icon_id = factory.LazyFunction(generate_random_string)
    revision_date = factory.LazyFunction(datetime.datetime.now)
    summoner_level = 100
