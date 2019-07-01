# Generated by Django 2.2.2 on 2019-07-01 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodtrack', '0015_auto_20190701_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='data_type',
            field=models.CharField(choices=[('market_acquisition', 'market_acquisition'), ('sample_food', 'sample_food'), ('agricultural_acquisition', 'agricultural_acquisition'), ('sub_sample_food', 'sub_sample_food'), ('survey_fndds_food', 'survey_fndds_food'), ('sr_legacy_food', 'sr_legacy_food'), ('foundation_food', 'foundation_food'), ('branded_food', 'branded_food')], max_length=2048),
        ),
        migrations.AlterField(
            model_name='nutritionprofiletarget',
            name='kind',
            field=models.IntegerField(choices=[(20, 'Daily Percentage'), (10, 'Daily Grams')]),
        ),
    ]