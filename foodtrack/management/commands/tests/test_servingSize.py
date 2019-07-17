from unittest import TestCase

from foodtrack.management.commands.parseRecipes import ServingSize


class TestServingSize(TestCase):

    def test_get1(self):
        self.assertEqual(ServingSize(" 1 serving ").get(), 1)

    def test_get2(self):
        self.assertEqual(ServingSize(" 8 servings ").get(), 8)

    def test_get3(self):
        self.assertEqual(ServingSize(" Varies ").get(), "Varies")
