# Generated by Django 2.2.2 on 2019-07-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodtrack', '0014_merge_20190701_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutritionprofiletarget',
            name='kind',
            field=models.IntegerField(choices=[(10, 'Daily Grams'), (20, 'Daily Percentage')], default=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='food',
            name='data_type',
            field=models.CharField(choices=[('market_acquisition', 'market_acquisition'), ('sub_sample_food', 'sub_sample_food'), ('survey_fndds_food', 'survey_fndds_food'), ('sample_food', 'sample_food'), ('branded_food', 'branded_food'), ('agricultural_acquisition', 'agricultural_acquisition'), ('sr_legacy_food', 'sr_legacy_food'), ('foundation_food', 'foundation_food')], max_length=2048),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='kind',
            field=models.IntegerField(choices=[(10, 'Food from DB'), (20, 'Other')]),
        ),
    ]