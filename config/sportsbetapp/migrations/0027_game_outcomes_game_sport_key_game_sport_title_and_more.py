# Generated by Django 4.1.7 on 2023-06-15 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbetapp', '0026_market'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='outcomes',
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='sport_key',
            field=models.CharField(default='[]', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='sport_title',
            field=models.CharField(default={}, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='away_team',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_team',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outcome_set', to='sportsbetapp.game'),
        ),
    ]
