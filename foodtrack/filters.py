from django_filters import FilterSet

from foodtrack.models import PurchaseItem


class FoodPurchaseItemFilter(FilterSet):

    class Meta:
        model = PurchaseItem
        fields = {
            "food": ['exact'],
            "store_name": ['exact', 'in'],
            "dt": ['exact', 'range']
        }

