# Generated by Django 4.1.7 on 2023-07-06 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("collector", "0010_matchparticipantbasicstats"),
    ]

    operations = [
        migrations.CreateModel(
            name="Match",
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
                ("game_id", models.CharField(max_length=250)),
                ("game_creation", models.DateTimeField()),
                ("game_start_timestamp", models.DateTimeField()),
                ("game_end_timestamp", models.DateTimeField()),
                ("game_mode", models.CharField(max_length=250)),
                ("game_name", models.CharField(max_length=250)),
                ("game_type", models.CharField(max_length=250)),
                ("game_version", models.CharField(max_length=250)),
                ("map_id", models.IntegerField()),
                ("platform_id", models.CharField(max_length=250)),
                ("queue_id", models.IntegerField()),
                ("teams", models.JSONField()),
                ("tournament_code", models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name="matchparticipantbasicstats",
            name="largest_multi_kill",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="matchparticipantbasicstats",
            name="win",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="MatchParticipantStats",
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
                ("champion_name", models.CharField(max_length=250)),
                ("total_damage_dealt", models.IntegerField()),
                ("total_damage_dealt_to_champions", models.IntegerField()),
                ("total_damage_taken", models.IntegerField()),
                ("magic_damage_dealt", models.IntegerField()),
                ("magic_damage_dealt_to_champions", models.IntegerField()),
                ("magic_damage_taken", models.IntegerField()),
                ("physical_damage_dealt", models.IntegerField()),
                ("physical_damage_dealt_to_champions", models.IntegerField()),
                ("physical_damage_taken", models.IntegerField()),
                ("total_heal", models.IntegerField()),
                ("total_minions_killed", models.IntegerField()),
                ("total_time_spent_dead", models.IntegerField()),
                ("true_damage_dealt", models.IntegerField()),
                ("true_damage_dealt_to_champions", models.IntegerField()),
                ("true_damage_taken", models.IntegerField()),
                ("turrent_kills", models.IntegerField()),
                ("turrent_takes", models.IntegerField()),
                ("turrents_lost", models.IntegerField()),
                ("vision_score", models.IntegerField()),
                ("vision_wards_bought_in_game", models.IntegerField()),
                ("wards_killed", models.IntegerField()),
                ("wards_placed", models.IntegerField()),
                ("gold_earned", models.IntegerField()),
                ("gold_spent", models.IntegerField()),
                ("longest_time_spent_living", models.IntegerField()),
                ("time_played", models.IntegerField()),
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
