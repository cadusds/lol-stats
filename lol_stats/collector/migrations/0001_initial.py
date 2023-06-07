# Generated by Django 4.1.7 on 2023-04-02 03:12

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Summoners",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("summoner_id", models.CharField(max_length=250)),
                ("account_id", models.CharField(max_length=250)),
                ("puuid", models.CharField(max_length=250)),
                ("name", models.CharField(max_length=250)),
                ("profile_icon_id", models.CharField(max_length=250)),
                ("revision_date", models.DateTimeField()),
                ("summoner_level", models.IntegerField()),
            ],
        ),
    ]
