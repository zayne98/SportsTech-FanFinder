# Generated by Django 3.2 on 2023-04-03 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='team_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
