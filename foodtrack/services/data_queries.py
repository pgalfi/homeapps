import datetime
from typing import Tuple

from django.db.models import QuerySet, Sum, F
from django.forms import Form

from foodtrack import constants


class QueryFormFilter:

    def __init__(self, query_set: QuerySet, frm: Form, empty_values: Tuple = ()):
        self.query_set = query_set
        self.frm = frm
        self.frm.full_clean()
        self.empty_values = empty_values

    def filter(self):
        for cleaned_field, cleaned_data in self.frm.cleaned_data.items():
            if cleaned_data in self.empty_values: continue
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


class QueryFoodPurchaseSummarizer:

    def __init__(self, query_set: QuerySet, summary_type: int):
        self.query_set = query_set
        self.summary_type = summary_type

    def summarize(self):
        if self.summary_type == constants.FOOD_PURCHASE_SUMM_ITEM_STORE \
                or self.summary_type == constants.FOOD_PURCHASE_SUMM_STORE_ITEM:
            self.query_set = self.query_set.values("food__description", "store_name", "currency__rate")
        elif self.summary_type == constants.FOOD_PURCHASE_SUMM_STORE:
            self.query_set = self.query_set.values("store_name", "currency__rate")
        elif self.summary_type == constants.FOOD_PURCHASE_SUMM_ITEM:
            self.query_set = self.query_set.values("food__description", "currency__rate")
        self.query_set = self.query_set.annotate(total=Sum(F("cost") * F("currency__rate")))
        if self.summary_type == constants.FOOD_PURCHASE_SUMM_ITEM_STORE:
            self.query_set = self.query_set.order_by("food__description", "store_name")
        elif self.summary_type == constants.FOOD_PURCHASE_SUMM_STORE_ITEM:
            self.query_set = self.query_set.order_by("store_name", "food__description")
        elif self.summary_type == constants.FOOD_PURCHASE_SUMM_ITEM:
            self.query_set = self.query_set.order_by("food__description")
        elif self.summary_type == constants.FOOD_PURCHASE_SUMM_STORE:
            self.query_set = self.query_set.order_by("store_name")
        return self.query_set
