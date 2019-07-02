# Generated by Django 2.2.2 on 2019-07-02 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodtrack', '0024_auto_20190702_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='total_gram',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='food',
            name='data_type',
            field=models.CharField(choices=[('foundation_food', 'foundation_food'), ('sr_legacy_food', 'sr_legacy_food'), ('market_acquisition', 'market_acquisition'), ('agricultural_acquisition', 'agricultural_acquisition'), ('branded_food', 'branded_food'), ('sub_sample_food', 'sub_sample_food'), ('survey_fndds_food', 'survey_fndds_food'), ('sample_food', 'sample_food')], max_length=2048),
        ),
        migrations.AlterField(
            model_name='nutrienttargets',
            name='kind',
            field=models.IntegerField(choices=[(10, 'Daily Grams'), (20, 'Daily Percentage')]),
        ),
        migrations.AlterField(
            model_name='nutritionprofiletarget',
            name='kind',
            field=models.IntegerField(choices=[(10, 'Daily Grams'), (20, 'Daily Percentage')]),
        ),
    ]
