# Generated by Django 5.0.4 on 2024-06-04 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rec', '0003_user_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilitator',
            name='contact',
        ),
    ]
