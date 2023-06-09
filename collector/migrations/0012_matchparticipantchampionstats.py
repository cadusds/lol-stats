# Generated by Django 4.1.7 on 2023-07-11 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "collector",
            "0011_match_matchparticipantbasicstats_largest_multi_kill_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="MatchParticipantChampionStats",
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
                ("champion_name", models.CharField(max_length=200)),
                ("champ_experience", models.IntegerField()),
                ("champ_level", models.IntegerField()),
                ("items_purchased", models.IntegerField()),
                ("item0", models.IntegerField()),
                ("item1", models.IntegerField()),
                ("item2", models.IntegerField()),
                ("item3", models.IntegerField()),
                ("item4", models.IntegerField()),
                ("item5", models.IntegerField()),
                ("item6", models.IntegerField()),
                ("spell1_casts", models.IntegerField()),
                ("spell2_casts", models.IntegerField()),
                ("spell3_casts", models.IntegerField()),
                ("spell4_casts", models.IntegerField()),
                (
                    "game_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="collector.summonermatch",
                    ),
                ),
                (
                    "summoner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="collector.summoner",
                    ),
                ),
            ],
        ),
    ]
