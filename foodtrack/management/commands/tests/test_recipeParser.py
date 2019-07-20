from unittest import TestCase

from foodtrack.management.commands.parseRecipes import RecipeParser, ParsedRecipe, Ingredient, ServingSize, PrepTime


class TestRecipeParser(TestCase):
    def test_00_parse(self):
        p = ParsedRecipe()
        p.name = "Bacon and Spinach Breakfast"
        p.desc = "The perfect keto breakfast: a combination of spinach, bacon, avocado, and eggs."
        p.prep_time = 30.0
        p.serving_size = 1
        p.ingredients = [Ingredient(food="Bacon", amount=4, unit="slices"),
                         Ingredient(food="Coconut Oil", amount=1, unit="tablespoon"),
                         Ingredient(food="Eggs", amount=2, unit="large eggs"),
                         Ingredient(food="Spinach", amount=2, unit="cups"),
                         Ingredient(food="Avocado", amount=.5, unit="medium avocado")]
        parsed = RecipeParser(r"c:\Users\admin\Downloads\test_recipe - 1.txt").parse()[0]
        self.assertEqual(p.name, parsed.name)
        self.assertEqual(p.desc, parsed.desc)
        self.assertEqual(p.prep_time, parsed.prep_time)
        self.assertEqual(p.serving_size, parsed.serving_size)
        for i in range(len(p.ingredients)):
            self.assertEqual(p.ingredients[i].food, parsed.ingredients[i].food)
            self.assertEqual(p.ingredients[i].amount, parsed.ingredients[i].amount)
            self.assertEqual(p.ingredients[i].unit, parsed.ingredients[i].unit)

    def test_01_parse(self):
        recipes = RecipeParser(r"c:\Users\admin\Downloads\test_recipe.txt").parse()
        self.assertEqual(3, len(recipes))
        self.assertEqual("Bacon and Spinach Breakfast", recipes[0].name)
        self.assertEqual("Sausage & Egg Biscuit", recipes[1].name)
        self.assertEqual(30, recipes[0].prep_time)
        self.assertEqual("Coconut Oil", recipes[2].ingredients[1].food)

    def test_zz_parse(self):
        recipes = RecipeParser(r"c:\Users\admin\Downloads\recipes.txt").parse()
        print([{"name": recipe.name, "time": recipe.prep_time} for recipe in recipes])
        self.assertEqual(120, len(recipes))
