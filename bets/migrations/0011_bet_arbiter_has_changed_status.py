# Generated by Django 5.2.1 on 2025-06-13 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0010_bet_opponent_accepted_alter_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='arbiter_has_changed_status',
            field=models.BooleanField(default=False),
        ),
    ]
