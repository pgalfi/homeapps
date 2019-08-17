from django.contrib.auth.models import User
from django.test import TestCase

from foodtrack.models import NutritionProfile, UserNutrition
from foodtrack.services import nutrients


class TestNutrientTargets(TestCase):
    fixtures = ["users.json", "nutrients.json", "measure-units.json", "user-nutrition.json"]

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.nutrition_profile = NutritionProfile.objects.get(pk=1)

    def test_generate(self):
        UserNutrition(user=self.user1, profile=self.nutrition_profile).save()
        nutrients.generate_nutrient_targets(self.user1)
        self.assertEqual(30, self.user1.nutrient_targets.get(nutrient_id=1005).amount)


