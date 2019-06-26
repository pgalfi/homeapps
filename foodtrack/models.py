from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Nutrient(models.Model):
    name = models.CharField(max_length=2048)
    unit = models.CharField(max_length=2048)


class MeasureUnit(models.Model):
    name = models.CharField(max_length=2048)


class FoodCategory(models.Model):
    code = models.IntegerField()
    description = models.CharField(max_length=2048)


class Food(models.Model):
    data_type = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField()


class FoodNutrientSource(models.Model):
    code = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)


class FoodNutrientDerivation(models.Model):
    code = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)
    source = models.ForeignKey(FoodNutrientSource, on_delete=models.CASCADE, null=True)


class FoodNutrient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()
    derivation = models.ForeignKey(FoodNutrientDerivation, on_delete=models.CASCADE, null=True)


class FoodPortion(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE)
    description = models.CharField(max_length=2048)
    modifier = models.CharField(max_length=2048)
    weight = models.FloatField()


class FoodLogCategory(models.Model):
    name = models.CharField(max_length=1024)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class FoodLogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    category = models.ForeignKey(FoodLogCategory, null=True, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    portion = models.ForeignKey(FoodPortion, on_delete=models.CASCADE)
    amount = models.FloatField()

# test 3