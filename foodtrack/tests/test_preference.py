from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase

from foodtrack.app_forms import FoodPurchaseForm
from foodtrack.models import PurchaseItem, UserPreference
from foodtrack.services.data_events import purchase_saved
from foodtrack.services.user_prefs import save_form_preference, load_form_preference


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
                                  "forms": {
                                      "foodpurchaseform": {
                                          "store_name": "APPLE",
                                          "unit": 99999,
                                      }
                                  }
                              })
        pref.save()

    def test_save_preference(self):
        purchase = PurchaseItem.objects.get(pk=1)
        user = User.objects.get(pk=1)
        fp_form = FoodPurchaseForm(instance=purchase, data={})
        save_form_preference(FoodPurchaseForm, fp_form.initial, user.id)
        user_pref = UserPreference.objects.get(pk=1)
        self.assertEqual("TEST", user_pref.prefs["forms"]["foodpurchaseform"]["store_name"])

    def test_load_preference(self):
        user = User.objects.get(pk=2)
        pref = load_form_preference(FoodPurchaseForm, user.id)
        self.assertEqual("APPLE", pref["store_name"])
        self.assertEqual(99999, pref["unit"])
