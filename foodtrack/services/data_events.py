from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from foodtrack.models import PurchaseItem, UsageCounter, Food


@receiver(post_save, sender=PurchaseItem)
def purchase_saved(sender, **kwargs):
    if kwargs["created"]:
        purchase: PurchaseItem = kwargs["instance"]
        add_food_usage_count(purchase.food, purchase.owner)
        # save_form_preference(purchase, purchase.owner_id)


def add_food_usage_count(food, user):
    content_type_food = ContentType.objects.get_for_model(Food)
    usage, created = UsageCounter.objects.get_or_create(defaults={"count": 1},
                                                        content_type=content_type_food,
                                                        object_id=food.id,
                                                        owner=user)
    if not created:
        usage.count += 1
        usage.save()
