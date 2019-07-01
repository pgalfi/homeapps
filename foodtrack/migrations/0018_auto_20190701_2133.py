# Generated by Django 2.2.2 on 2019-07-01 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodtrack', '0017_auto_20190701_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipecomponent',
            name='custom_food',
        ),
        migrations.AddField(
            model_name='recipe',
            name='serving_amount',
            field=models.FloatField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='serving_size',
            field=models.ForeignKey(default=1049, on_delete=django.db.models.deletion.CASCADE, to='foodtrack.MeasureUnit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipecomponent',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='components', to='foodtrack.Recipe'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='food',
            name='data_type',
            field=models.CharField(choices=[('sample_food', 'sample_food'), ('agricultural_acquisition', 'agricultural_acquisition'), ('survey_fndds_food', 'survey_fndds_food'), ('foundation_food', 'foundation_food'), ('market_acquisition', 'market_acquisition'), ('sr_legacy_food', 'sr_legacy_food'), ('sub_sample_food', 'sub_sample_food'), ('branded_food', 'branded_food')], max_length=2048),
        ),
        migrations.CreateModel(
            name='RecipeComputedNutrient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('nutrient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodtrack.Nutrient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutrients', to='foodtrack.Recipe')),
            ],
        ),
    ]
