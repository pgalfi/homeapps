# Generated by Django 2.2.2 on 2019-06-26 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodtrack', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FoodLogEntry',
        ),
    ]
