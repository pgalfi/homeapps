from unittest import TestCase, mock

from django.db.models import Sum, F

from foodtrack import constants
from foodtrack.services.data_queries import QueryFoodPurchaseSummarizer


class TestQueryFoodPurchaseSummarizer(TestCase):

    def setUp(self) -> None:
        self.qs = mock.MagicMock()
        self.qs.values = mock.Mock(return_value=self.qs)
        self.qs.order_by = mock.Mock(return_value=self.qs)
        self.qs.annotate = mock.Mock(return_value=self.qs)

    def test_01(self):
        query_summarizer = QueryFoodPurchaseSummarizer(query_set=self.qs, summary_type=0)
        self.qs = query_summarizer.apply()
        self.assertFalse(self.qs.values.called)
        self.assertFalse(self.qs.order_by.called)

    def test_02(self):
        query_summarizer = QueryFoodPurchaseSummarizer(query_set=self.qs,
                                                       summary_type=constants.FOOD_PURCHASE_SUMM_ITEM_STORE)
        self.qs = query_summarizer.apply()
        self.qs.values.assert_any_call("food__description", "store_name", "currency__rate")
        self.qs.order_by.assert_any_call("food__description", "store_name")
        self.qs.annotate.assert_any_call(total=Sum(F("cost") * F("currency__rate")))
