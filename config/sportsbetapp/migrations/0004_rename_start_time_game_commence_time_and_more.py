# Generated by Django 4.1.7 on 2023-05-31 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbetapp', '0003_remove_game_name_game_away_team_game_home_team_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='start_time',
            new_name='commence_time',
        ),
        migrations.RemoveField(
            model_name='game',
            name='details',
        ),
        migrations.AlterField(
            model_name='game',
            name='away_team',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_team',
            field=models.CharField(max_length=200),
        ),
    ]
