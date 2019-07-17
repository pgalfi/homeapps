from unittest import TestCase

from foodtrack.management.commands.parseRecipes import Ingredient


class TestIngredient(TestCase):
    def test_get1(self):
        line = "Cream cheese - 2 tablespoons"
        ingredient = Ingredient(line)
        data = ingredient.get()
        self.assertEqual(data["food"], "Cream cheese")
        self.assertEqual(data["amount"], 2)
        self.assertEqual(data["unit"], "tablespoons")

    def test_get2(self):
        line = "Coconut Flour - 1/4 cup "
        ingredient = Ingredient(line)
        data = ingredient.get()
        self.assertEqual(data["food"], "Coconut Flour")
        self.assertEqual(data["amount"], 0.25)
        self.assertEqual(data["unit"], "cup")

    def test_get3(self):
        line = "Hazelnut Butter- 1 ½ tablespoons  "
        ingredient = Ingredient(line)
        data = ingredient.get()
        self.assertEqual(data["food"], "Hazelnut Butter")
        self.assertEqual(data["amount"], 1.5)
        self.assertEqual(data["unit"], "tablespoons")

    def test_get4(self):
        line = "Parmesan Cheese - 1 cup - grated "
        ingredient = Ingredient(line)
        data = ingredient.get()
        self.assertEqual(data["food"], "Parmesan Cheese")
        self.assertEqual(data["amount"], 1)
        self.assertEqual(data["unit"], "cup - grated")

