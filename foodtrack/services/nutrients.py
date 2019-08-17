import datetime

from foodtrack import constants
from foodtrack.models import FoodLogEntryNutrient, FoodLogEntry, FoodNutrient, RecipeComputedNutrient, UserNutrition, \
    NutrientTargets, NutritionProfileTarget


def build_nutrients(log_entry: FoodLogEntry):
    FoodLogEntryNutrient.objects.filter(entry=log_entry).delete()

    if log_entry.food is not None:
        food_nutrient_set = list(FoodNutrient.objects.filter(food=log_entry.food, amount__gt=0))
        if log_entry.portion.id == 1:
            gr_ratio = log_entry.amount / 100
        else:
            gr_ratio = (log_entry.portion.gram_weight * log_entry.amount) / 100
    else:
        food_nutrient_set = list(RecipeComputedNutrient.objects.filter(recipe=log_entry.alt_food, ))
        # Take into account "serving" portion for the recipe foods, it won't be in gram
        gr_ratio = (log_entry.amount * (log_entry.alt_food.total_gram / log_entry.alt_food.serving_amount)) / 100
    entry_nutrients = []
    for food_nutrient in food_nutrient_set:
        nutrient_entry = FoodLogEntryNutrient(entry=log_entry)
        nutrient_entry.nutrient = food_nutrient.nutrient
        nutrient_entry.amount = gr_ratio * food_nutrient.amount
        entry_nutrients.append(nutrient_entry)
    FoodLogEntryNutrient.objects.bulk_create(entry_nutrients)


def compute_nutrients(recipe):
    # Clear any earlier nutrient calculation
    RecipeComputedNutrient.objects.filter(recipe=recipe).delete()
    nutrients_data = list(recipe.components.filter(food__nutrients__amount__gt=0)
                          .values("food_id", "amount", "portion__gram_weight",
                                  "food__nutrients__nutrient__id", "food__nutrients__amount"))
    recipe_nutrients = {}
    food_weights = {}
    for food_nutrient in nutrients_data:
        if food_nutrient["food__nutrients__amount"] <= 0: continue
        if food_nutrient["portion__gram_weight"] is None:
            food_nutrient["portion__gram_weight"] = 1
        # grams of that food in the recipe
        food_gram = food_nutrient["amount"] * food_nutrient["portion__gram_weight"]
        # save the gram of that food from the recipe
        if food_nutrient["food_id"] not in food_weights:
            food_weights[food_nutrient["food_id"]] = food_gram
        # total volume of that nutrient in the total amount of food.
        recipe_nutrient_amount = food_gram * (food_nutrient["food__nutrients__amount"] / 100)
        if food_nutrient["food__nutrients__nutrient__id"] not in recipe_nutrients:
            recipe_nutrient = RecipeComputedNutrient(recipe=recipe,
                                                     nutrient_id=food_nutrient["food__nutrients__nutrient__id"],
                                                     amount=recipe_nutrient_amount)
            recipe_nutrients[food_nutrient["food__nutrients__nutrient__id"]] = recipe_nutrient
        else:
            recipe_nutrients[food_nutrient["food__nutrients__nutrient__id"]].amount += recipe_nutrient_amount

    # Total nutrient volumes need to be now calculated from total recipe weight to 100 gr weight
    recipe.total_gram = sum([food_weights[food_id] for food_id in food_weights.keys()])
    recipe.save()
    # establish ratio to 100g
    recipe_ratio = 100 / recipe.total_gram
    # set nutrient amounts with the ratio to represent per 100g values
    for recipe_nutrient in recipe_nutrients.values():
        recipe_nutrient.amount = recipe_nutrient.amount * recipe_ratio
    recipe_nutrients_list = [recipe_nutrient for recipe_nutrient in recipe_nutrients.values()]
    RecipeComputedNutrient.objects.bulk_create(recipe_nutrients_list)


def generate_nutrient_targets(user):
    day = datetime.date.today()
    try:
        user_profile = UserNutrition.objects.get(user=user)
    except UserNutrition.DoesNotExist:
        return
    # check if targets have already been calculated
    existing_targets = NutrientTargets.objects.filter(user=user, day=day)
    profile = user_profile.profile
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
