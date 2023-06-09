# Generated by Django 4.1.7 on 2023-06-20 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("collector", "0009_alter_summonermatch_game_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="MatchParticipantBasicStats",
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
                ("team_position", models.CharField(max_length=200)),
                ("deaths", models.IntegerField()),
                ("assists", models.IntegerField()),
                ("kills", models.IntegerField()),
                ("double_kills", models.IntegerField()),
                ("triple_kills", models.IntegerField()),
                ("quadra_kills", models.IntegerField()),
                ("penta_kills", models.IntegerField()),
                ("first_blood_kill", models.BooleanField()),
                ("first_blood_assist", models.BooleanField()),
                ("first_tower_kill", models.BooleanField()),
                ("first_tower_assist", models.BooleanField()),
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
