import datetime
from unittest import mock, TestCase

from django.forms import Form, IntegerField, DateField

from foodtrack.services.data_queries import QuerySetFormFilter


class TestQuerySetFormFilter(TestCase):

    def setUp(self) -> None:
        self.qs = mock.MagicMock()
        self.qs.filter = mock.Mock(return_value=self.qs)

    def test_filter_01(self):
        class TestForm(Form):
            basic = IntegerField()

        test_form = TestForm(data={"basic": 3})
        query_filter = QuerySetFormFilter(self.qs, test_form)
        self.assertTrue("basic" in test_form.cleaned_data)
        self.assertEqual(test_form.cleaned_data["basic"], 3)
        self.qs = query_filter.apply()
        self.qs.filter.assert_called_with(basic=3)

    def test_filter_02(self):
        class TestForm(Form):
            basic = IntegerField()
            birth_date_start = DateField()
            birth_date_end = DateField()

        test_form = TestForm(data={"basic": 3, "birth_date_start": "2001-01-01"})
        query_filter = QuerySetFormFilter(self.qs, test_form)
        self.assertTrue("basic" in test_form.cleaned_data)
        self.assertEqual(test_form.cleaned_data["basic"], 3)
        self.assertTrue("birth_date_start" in test_form.cleaned_data)
        self.assertEqual(test_form.cleaned_data["birth_date_start"], datetime.date(2001,1,1))
        self.assertTrue("birth_date_end" not in test_form.cleaned_data)
        self.qs = query_filter.apply()
        self.qs.filter.assert_any_call(basic=3)
        self.qs.filter.assert_any_call(birth_date__gte=datetime.date(2001,1,1))

