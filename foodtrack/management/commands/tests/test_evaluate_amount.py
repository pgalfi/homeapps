from unittest import TestCase

from foodtrack.management.commands.parseRecipes import evaluate_amount


class TestEvaluateAmount(TestCase):

    def test_evaluate1(self):
        self.assertEqual(evaluate_amount("2"), 2)

    def test_evaluate2(self):
        self.assertEqual(evaluate_amount("5-6"), 5.5)

    def test_evaluate3(self):
        self.assertEqual(evaluate_amount("½"), 0.5)

    def test_evaluate4(self):
        self.assertEqual(evaluate_amount("1 ½"), 1.5)

    def test_evaluate5(self):
        self.assertEqual(evaluate_amount("1/2"), 0.5)

    def test_evaluate6(self):
        self.assertEqual(evaluate_amount("5:30"), 5.5)

