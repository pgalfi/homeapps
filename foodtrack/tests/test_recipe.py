from django.contrib.auth.models import User
from django.test import TestCase

from foodtrack import services
from foodtrack.models import Recipe


class TestRecipe(TestCase):
    fixtures = ["users.json", "nutrients.json", 'food-categories.json', 'measure-units.json',
                'nutrient-derivations.json', 'food.json', 'food-portions.json', 'food-nutrients.json',
                'recipes.json']

    def setUp(self) -> None:
        self.user1 = User.objects.get(pk=1)
        self.recipe = Recipe.objects.get(pk=1)

    def test_01_created_recipe(self):
        self.assertEqual("Tomatoes a la Olive", self.recipe.name)

    def test_02_added_recipe_components(self):
        self.assertEqual("Tomatoes, red, ripe, raw, year round average",self.recipe.components.all()[0].food.description)

    def test_03_compute_nutrients(self):
        services.compute_nutrients(self.recipe)
        # 4 x medium tomatos = 492g + 8 x tbsp olive oil = 108g = 600g
        # tomato carb = 4.92 * 3.89g = 19.1388g + 1.08 * 0.1 = 0.108g --> total =19.2468g for total
        # recipe 100g carb amount = 3.2078g
        self.assertEqual(600, self.recipe.total_gram)
        self.assertEqual(3.2078, round(self.recipe.nutrients.get(nutrient_id=1005).amount, 4))

