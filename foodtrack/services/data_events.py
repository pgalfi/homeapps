from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from foodtrack.models import PurchaseItem, FoodUsageCounter
from foodtrack.services.user_prefs import save_model_preference


@receiver(post_save, sender=PurchaseItem)
def purchase_saved(sender, **kwargs):
    if kwargs["created"]:
        purchase: PurchaseItem = kwargs["instance"]
        add_food_usage_count(purchase.food, purchase.owner)
        save_model_preference(purchase, purchase.owner_id)


def add_food_usage_count(food, user):
    usage, created = FoodUsageCounter.objects.get_or_create(
        defaults={"food": food, "owner": user, "count": 1},
        food=food, owner=user)
    if not created:
        usage.update(count=F('count') + 1)
