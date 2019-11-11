from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from foodtrack.models import Food
from foodtrack.services.data_proxies import create_usage_proxy


class TestCreateUsageProxy(TestCase):
    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json',
                'nutrient-derivations.json', 'food.json', 'food-portions.json', 'food-nutrients.json',
                'usage-counter.json']

    def test_check_content_types(self):
        foodType = ContentType.objects.get_for_model(model=Food)
        self.assertEqual(8, foodType.id)

    def test_create_usage_proxy(self):
        food = Food.objects.get(pk=170457)
        self.assertEqual(11, food.category.id)
        FoodProxy = create_usage_proxy(owner_id=2, base_model=Food)
        foodp = FoodProxy.objects.filter(id=170457).values_list("category_id", "usage__count")
        self.assertEqual(11, foodp[0][0])
        self.assertEqual(30, foodp[0][1])
