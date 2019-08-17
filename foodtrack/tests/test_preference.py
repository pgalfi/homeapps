from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase

from foodtrack.models import PurchaseItem, UserPreference
from foodtrack.services.data_events import purchase_saved
from foodtrack.services.user_prefs import save_model_preference, load_model_preference


class TestPreferences(TestCase):

    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json', 'food.json',
                'currency.json', 'purchase-items.json']

    @classmethod
    def setUpClass(cls):
        post_save.disconnect(purchase_saved, sender=PurchaseItem)
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        pref = UserPreference(owner_id=2,
                              prefs={
                                  "models": {
                                      "purchaseitem": {
                                          "store_name": "APPLE",
                                          "unit_id": 99999,
                                      }
                                  }
                              })
        pref.save()

    def test_save_preference(self):
        purchase = PurchaseItem.objects.get(pk=1)
        user = User.objects.get(pk=1)
        save_model_preference(purchase, user.id)
        user_pref = UserPreference.objects.get(pk=1)
        self.assertEqual("TEST", user_pref.prefs["models"]["purchaseitem"]["store_name"])

    def test_load_preference(self):
        user = User.objects.get(pk=2)
        pref = load_model_preference(PurchaseItem, user.id)
        self.assertEqual("APPLE", pref["store_name"])
        self.assertEqual(99999, pref["unit_id"])
