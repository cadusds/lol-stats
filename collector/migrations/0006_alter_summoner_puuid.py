# Generated by Django 4.1.7 on 2023-05-10 01:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collector", "0005_remove_summoner_id_alter_summoner_puuid_match_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="summoner",
            name="puuid",
            field=models.CharField(
                editable=False, max_length=250, primary_key=True, serialize=False
            ),
        ),
    ]