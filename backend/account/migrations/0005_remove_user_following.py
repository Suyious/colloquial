# Generated by Django 5.0.6 on 2024-07-04 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_followers_alter_user_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
    ]
