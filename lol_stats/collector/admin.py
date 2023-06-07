from django.contrib import admin
from django.apps import apps


collector_models = apps.get_app_config("collector").get_models()

for model in collector_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
