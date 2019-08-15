from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from foodtrack import services
from foodtrack.models import Food, FoodLogEntry, FoodLogCategory


class TestFoodLogEntryNutrient(TestCase):
    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json',
                'nutrient-derivations.json', 'food.json', 'food-portions.json', 'food-nutrients.json',
                'food-log-categories.json']

    def setUp(self) -> None:
        self.tomato_red = Food.objects.get(pk=170457)
        self.one_user = User.objects.get(pk=1)

    def test_data_load(self):
        self.assertEqual("Tomatoes, red, ripe, raw, year round average",self.tomato_red.description)
        self.assertEqual(3.89, self.tomato_red.nutrients.get(nutrient_id=1005).amount)
        self.assertEqual("Breakfast", FoodLogCategory.objects.get(pk=1).name)

    def test_nutrient_calculation_1(self):
        food_log_entry_1 = FoodLogEntry(food=self.tomato_red, user=self.one_user, dt=timezone.now(),
                                        category_id=1, amount=1, portion_id=86681)
        food_log_entry_1.save()
        services.build_nutrients(food_log_entry_1)
        self.assertEqual(5.7961, food_log_entry_1.nutrients.get(nutrient_id=1005).amount)

    def test_nutrient_calculation_2(self):
        food_log_entry_2 = FoodLogEntry(food=self.tomato_red, user=self.one_user, dt=timezone.now(),
                                        category_id=1, amount=10, portion_id=86684)
        food_log_entry_2.save()
        services.build_nutrients(food_log_entry_2)
        self.assertEqual(6.613, food_log_entry_2.nutrients.get(nutrient_id=1005).amount)


