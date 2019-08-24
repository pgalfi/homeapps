from django.db.models.signals import post_save
from django.dispatch import receiver

from foodtrack.models import PurchaseItem, FoodUsageCounter


@receiver(post_save, sender=PurchaseItem)
def purchase_saved(sender, **kwargs):
    if kwargs["created"]:
        purchase: PurchaseItem = kwargs["instance"]
        add_food_usage_count(purchase.food, purchase.owner)
        # save_form_preference(purchase, purchase.owner_id)


def add_food_usage_count(food, user):
    usage, created = FoodUsageCounter.objects.get_or_create(
        defaults={"food": food, "owner": user, "count": 1},
        food=food, owner=user)
    if not created:
        usage.count += 1
        usage.save()
