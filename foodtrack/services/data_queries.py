import datetime
from abc import ABC, abstractmethod

from django.db.models import QuerySet, Sum, F
from django.forms import Form

from foodtrack import constants


class QuerySetChanger(ABC):

    def __init__(self, query_set: QuerySet, data=None, **kwargs):
        self.query_set = query_set
        self.data = data

    @abstractmethod
    def apply(self):
        pass


class QuerySetFormFilter(QuerySetChanger):

    def __init__(self, query_set: QuerySet, frm: Form):
        super().__init__(query_set, data=frm)
        self.data.full_clean()

    def apply(self):
        for cleaned_field, cleaned_data in self.data.cleaned_data.items():
            if cleaned_data in ('', None): continue
            if isinstance(cleaned_data, datetime.date) or isinstance(cleaned_data, datetime.datetime):
                if "_start" in cleaned_field:
                    self.query_set = self.query_set.filter(
                        **{cleaned_field.replace("_start", "") + "__gte": cleaned_data})
                elif "_end" in cleaned_field:
                    self.query_set = self.query_set.filter(
                        **{cleaned_field.replace("_end", "") + "__lte": cleaned_data})
                else:
                    self.query_set = self.query_set.filter(**{cleaned_field: cleaned_data})
            else:
                self.query_set = self.query_set.filter(**{cleaned_field: cleaned_data})
        return self.query_set


class QueryFoodPurchaseSummarizer(QuerySetChanger):

    def __init__(self, query_set: QuerySet, summary_type: int):
        super().__init__(query_set, data=summary_type)

    def apply(self):
        if self.data == constants.FOOD_PURCHASE_SUMM_ITEM_STORE \
                or self.data == constants.FOOD_PURCHASE_SUMM_STORE_ITEM:
            self.query_set = self.query_set.values("food__description", "store_name", "currency__rate")
        elif self.data == constants.FOOD_PURCHASE_SUMM_STORE:
            self.query_set = self.query_set.values("store_name", "currency__rate")
        elif self.data == constants.FOOD_PURCHASE_SUMM_ITEM:
            self.query_set = self.query_set.values("food__description", "currency__rate")
        self.query_set = self.query_set.annotate(total=Sum(F("cost") * F("currency__rate")))
        if self.data == constants.FOOD_PURCHASE_SUMM_ITEM_STORE:
            self.query_set = self.query_set.order_by("food__description", "store_name")
        elif self.data == constants.FOOD_PURCHASE_SUMM_STORE_ITEM:
            self.query_set = self.query_set.order_by("store_name", "food__description")
        elif self.data == constants.FOOD_PURCHASE_SUMM_ITEM:
            self.query_set = self.query_set.order_by("food__description")
        elif self.data == constants.FOOD_PURCHASE_SUMM_STORE:
            self.query_set = self.query_set.order_by("store_name")
        return self.query_set
