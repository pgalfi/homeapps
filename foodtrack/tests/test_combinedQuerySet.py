from django.db.models import Q
from django.test import TestCase

from foodtrack.models import Food, Recipe
from foodtrack.services.data_combination import CombinedQuerySet


class TestCombinedQuerySet(TestCase):

    def setUp(self) -> None:
        self.maxDiff = 4096

    def test_clean_filter_args_01(self):
        cqs = CombinedQuerySet(Food.objects.all(), Recipe.objects.all())
        test_query = Q(name__icontains="apple") | Q(description__iexact="bear")
        cqs.clean_filter_args([test_query], Food.objects.all())
        self.assertEqual("", str(test_query))

    def test_clean_filter_args_02(self):
        cqs = CombinedQuerySet(Food.objects.all(), Recipe.objects.all())
        test_query = Q(Q(name__icontains="apple") | Q(description__iexact="bear")) & Q(bird__iexact=12)
        cqs.clean_filter_args([test_query], Food.objects.all())
        self.assertEqual("", str(test_query))

