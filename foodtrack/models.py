import datetime

from django.contrib.auth.models import User
from django.db import models

from foodtrack import constants


# from USDA database
class Nutrient(models.Model):
    name = models.CharField(max_length=2048)
    unit = models.CharField(max_length=2048)

    def __str__(self):
        return self.name + " (" + self.unit + ")"


# from USDA database - added the "kind" field to identify the type of measurement (volume/weight)
class MeasureUnit(models.Model):
    name = models.CharField(max_length=2048)
    kind = models.IntegerField(choices=constants.MEASURE_KINDS, default=constants.MEASURE_OTHER)

    def __str__(self):
        return self.name


# standard conversion rate for volume->volume and weight->weight conversion
# provides ratios to the "liter" for volume and to the "gram" for weight
class UnitConversion(models.Model):
    unit = models.OneToOneField(to=MeasureUnit, on_delete=models.CASCADE)
    ratio = models.FloatField(null=True, default=None)

    @staticmethod
    def get_conversions():
        conversions = list(UnitConversion.objects.filter(ratio__isnull=False)
                           .values("unit_id", "unit__name", "unit__kind", "ratio"))
        conversion_table = {conversion["unit_id"]: conversion for conversion in conversions}
        return conversion_table


# from USDA database
class FoodCategory(models.Model):
    code = models.IntegerField()
    description = models.CharField(max_length=2048)

    def __str__(self):
        return self.description


# from USDA database
class Food(models.Model):
    data_type = models.CharField(max_length=2048, choices=constants.FOOD_DATA_TYPES)
    description = models.CharField(max_length=2048)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.description


# from USDA database
class FoodNutrientSource(models.Model):
    code = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)


# from USDA database
class FoodNutrientDerivation(models.Model):
    code = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)
    source = models.ForeignKey(FoodNutrientSource, on_delete=models.CASCADE, null=True)


# from USDA database, values are for 100g of food
class FoodNutrient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='nutrients')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()
    derivation = models.ForeignKey(FoodNutrientDerivation, on_delete=models.CASCADE, null=True)


# from USDA database
class FoodPortion(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=2048)
    modifier = models.CharField(max_length=2048)
    gram_weight = models.FloatField()

    def name(self):
        if len(self.description.strip())>0:
            return self.description
        elif self.amount != 1:
            return str(self.amount) + " " + self.modifier
        else:
            return self.modifier

    def __str__(self):
        return self.name


# Models for tracking food purchase
class Currency(models.Model):
    name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=1024, null=True)
    rate = models.FloatField()  # rate to base currency from constants.BASE_CURRENCY
    rate_date = models.DateTimeField()  # recorded for future extension for dynamic rate updates

    def __str__(self):
        return self.name


class PurchaseItem(models.Model):
    kind = models.IntegerField(choices=constants.PURCHASE_ITEM_KINDS)
    food = models.ForeignKey(Food, default=None, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=2048, default=None, null=True)
    pcs = models.IntegerField(verbose_name="Pieces", null=True, default=None)
    amount = models.FloatField(null=True)
    unit = models.ForeignKey(MeasureUnit, null=True, default=None, on_delete=models.SET_NULL)
    cost = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    dt = models.DateTimeField()


# categories set up by the user for daily food logging,
# default categories would be added with null owner
class FoodLogCategory(models.Model):
    name = models.CharField(max_length=1024)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# data logged by user on what was consumed and when
class FoodLogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    category = models.ForeignKey(FoodLogCategory, null=True, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, null=True, on_delete=models.CASCADE)
    alt_food = models.ForeignKey('Recipe', null=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    portion = models.ForeignKey(FoodPortion, null=True, on_delete=models.SET_NULL)


# nutrients calculated for each food log entry automatically
# based on the food and amount entered by the user
class FoodLogEntryNutrient(models.Model):
    entry = models.ForeignKey(FoodLogEntry, on_delete=models.CASCADE, related_name="nutrients")
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()

    @staticmethod
    def build_nutrients(log_entry):
        FoodLogEntryNutrient.objects.filter(entry=log_entry).delete()

        if log_entry.food is not None:
            foodnutrient_set = list(FoodNutrient.objects.filter(food=log_entry.food, amount__gt=0))
        else:
            foodnutrient_set = list(RecipeComputedNutrient.objects.filter(recipe=log_entry.alt_food, ))
        entry_nutrients = []
        if log_entry.portion.id==1:
            gr_ratio = log_entry.amount / 100
        else:
            gr_ratio = log_entry.portion.gram_weight / 100
        for foodnutrient in foodnutrient_set:
            nutrient_entry = FoodLogEntryNutrient(entry=log_entry)
            nutrient_entry.nutrient = foodnutrient.nutrient
            nutrient_entry.amount = gr_ratio * foodnutrient.amount
            entry_nutrients.append(nutrient_entry)
        FoodLogEntryNutrient.objects.bulk_create(entry_nutrients)



# nutrient targets for that user for a certain day
# to be automatically generated based on a nutrition profile for that day
class NutrientTargets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.DateField()
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()
    kind = models.IntegerField(choices=constants.NUTRIENT_TARGET_TYPES)
    notes = models.TextField(null=True)

    #TODO: Static method needs to be created that runs maintenance and clears out old daily targets

    @staticmethod
    def generate(user):
        day = datetime.date.today()
        try:
            userprofile = UserNutrition.objects.get(user=user)
        except UserNutrition.DoesNotExist:
            return
        # check if targets have already been calculated
        existing_targets = NutrientTargets.objects.filter(user=user, day=day)
        profile = userprofile.profile
        if profile.kind == constants.DAILY_TARGETS and existing_targets.count() > 0: return
        target_set = NutritionProfileTarget.objects.filter(profile=profile)
        if profile.kind == constants.DAILY_TARGETS:
            for target in target_set:
                nutrient_target = NutrientTargets(user=user, day=day)
                nutrient_target.nutrient = target.nutrient
                nutrient_target.kind = target.kind
                nutrient_target.amount = target.amount
                nutrient_target.notes = target.notes
                nutrient_target.save()

# a profile for a kind a nutrition plan that will include targets
# for each nutrient
class NutritionProfile(models.Model):
    name = models.CharField(max_length=1024)
    kind = models.IntegerField(choices=constants.PROFILE_TYPES)

    def __str__(self):
        return self.name


# nutrient target under a specific nutrition profile
class NutritionProfileTarget(models.Model):
    profile = models.ForeignKey(NutritionProfile, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()
    kind = models.IntegerField(choices=constants.NUTRIENT_TARGET_TYPES)
    notes = models.TextField(null=True)


# nutrition configuration data for a user
class UserNutrition(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(NutritionProfile, null=True, on_delete=models.SET_NULL)


# custom recipe based on existing foods
class Recipe(models.Model):
    name = models.CharField(max_length=2048)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    serving_amount = models.FloatField()

    def __str__(self):
        return self.name

    def compute_nutrients(self):
        nutrients_data = list(self.components.filter(food__nutrients__amount__gt=0)
                              .values("food_id", "amount", "portion__gram_weight",
                                      "food__nutrients__nutrient__id", "food__nutrients__amount"))
        recipe_nutrients = {}
        for food_nutrient in nutrients_data:
            if food_nutrient["food__nutrients__amount"] <= 0: continue
            if food_nutrient["portion__gram_weight"] is None:
                food_nutrient["portion__gram_weight"] = 1
            recipe_multiplier = food_nutrient["amount"] * food_nutrient["portion__gram_weight"]
            recipe_nutrient_amount = recipe_multiplier * (food_nutrient["food__nutrients__amount"] / 100)
            if food_nutrient["food__nutrients__nutrient__id"] not in recipe_nutrients:
                recipe_nutrient = RecipeComputedNutrient(recipe=self,
                                                         nutrient_id=food_nutrient["food__nutrients__nutrient__id"],
                                                         amount=recipe_nutrient_amount)
                recipe_nutrients[food_nutrient["food__nutrients__nutrient__id"]] = recipe_nutrient
            else:
                recipe_nutrients[food_nutrient["food__nutrients__nutrient__id"]].amount += recipe_nutrient_amount
        recipe_nutrients_list = [recipe_nutrient for recipe_nutrient in recipe_nutrients.values()]
        RecipeComputedNutrient.objects.bulk_create(recipe_nutrients_list)


class RecipeComponent(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='components')
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, default=None, related_name="components")
    amount = models.FloatField()  # default is grams if portion is null
    portion = models.ForeignKey(FoodPortion, on_delete=models.SET_NULL, null=True, default=None)


class RecipeComputedNutrient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='nutrients')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()


# TODO: Create Order classes for selectable elements such as Food, Nutrient etc.

# order of displaying nutrients based on recurring usage
class NutrientOrder(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
