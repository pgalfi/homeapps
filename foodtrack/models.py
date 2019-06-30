from django.contrib.auth.models import User
from django.db import models

from foodtrack import constants


# from USDA database
class Nutrient(models.Model):
    name = models.CharField(max_length=2048)
    unit = models.CharField(max_length=2048)


# from USDA database
class MeasureUnit(models.Model):
    name = models.CharField(max_length=2048)


# from USDA database
class FoodCategory(models.Model):
    code = models.IntegerField()
    description = models.CharField(max_length=2048)


# from USDA database
class Food(models.Model):
    data_type = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField()


# from USDA database
class FoodNutrientSource(models.Model):
    code = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)


# from USDA database
class FoodNutrientDerivation(models.Model):
    code = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)
    source = models.ForeignKey(FoodNutrientSource, on_delete=models.CASCADE, null=True)


# from USDA database
class FoodNutrient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='nutrients')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()
    derivation = models.ForeignKey(FoodNutrientDerivation, on_delete=models.CASCADE, null=True)


# from USDA database
class FoodPortion(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE)
    description = models.CharField(max_length=2048)
    modifier = models.CharField(max_length=2048)
    gram_weight = models.FloatField()


class RecentSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# categories set up by the user for daily food logging,
# default categories would be added with null owner
class FoodLogCategory(models.Model):
    name = models.CharField(max_length=1024)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


# data logged by user on what was consumed and when
class FoodLogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    category = models.ForeignKey(FoodLogCategory, null=True, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE)
    amount = models.FloatField()


# nutrients calculated for each food log entry automatically
# based on the food and amount entered by the user
class FoodLogEntryNutrients(models.Model):
    entry = models.ForeignKey(FoodLogEntry, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()


# nutrient targets for that user for a certain day
# to be automatically generated based on a nutrition profile for that day
class NutrientTargets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.DateField()
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()
    notes = models.TextField(null=True)


# a profile for a kind a nutrition plan that will include targets
# for each nutrient
class NutritionProfile(models.Model):
    name = models.CharField(max_length=1024)
    kind = models.IntegerField(choices=constants.PROFILE_TYPES)


# nutrient target under a specific nutrition profile
class NutritionProfileTargets(models.Model):
    profile = models.ForeignKey(NutritionProfile, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()
    notes = models.TextField(null=True)


# nutrition configuration data for a user
class UserNutrition(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(NutritionProfile, null=True, on_delete=models.SET_NULL)


# TODO: Create Order classes for selectable elements such as Food, Nutrient etc.

# order of displaying nutrients based on recurring usage
class NutrientOrder(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

