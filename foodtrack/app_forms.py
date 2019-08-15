import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Hidden, HTML, Field, Div
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from rest_framework.reverse import reverse

from foodtrack import constants
from foodtrack.models import PurchaseItem, FoodUsageCounter


class FoodTrackAuthForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_errors = False
        self.helper.layout = Layout(
            Fieldset("<h4>Authentication Required</h4>",
                     "username", "password"),
            Hidden("next", "/foodtrack/index/"),
            ButtonHolder(
                Submit("submit", "Login", css_class="btn-block")
            )
        )


class FoodTrackPasswordChangeForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset("<h4>Change Password</h4>",
                     "old_password", "new_password1", "new_password2"),
            ButtonHolder(
                Submit("submit", "Change Password", css_class="btn-block")
            )
        )


class FoodPurchaseForm(forms.ModelForm):
    description = forms.CharField(required=False)
    pcs = forms.IntegerField(min_value=1)
    amount = forms.FloatField(min_value=0.0001)
    cost = forms.FloatField(min_value=0.0001)

    class Meta:
        model = PurchaseItem
        fields = ["kind", "food", "description", "pcs", "amount", "unit", "cost", "currency", "store_name", "dt"]
        widgets = {
            "food": forms.TextInput,
            "dt": forms.TextInput(
                attrs={"type": "date"}
            ),
        }
        labels = {
            "dt": "Purchase date"
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial", {})
        if "user_preference" in initial:
            self.user_pref = initial["user_preference"]
            if "purchase" in initial["user_preference"].prefs:
                initial["unit"] = self.user_pref.prefs["purchase"]["unit_id"] \
                    if "unit_id" in self.user_pref.prefs["purchase"] else constants.DEFAULT_UNIT_ID
                initial["store_name"] = self.user_pref.prefs["purchase"]["store"] \
                    if "store" in self.user_pref.prefs["purchase"] else ""
                initial["currency"] = self.user_pref.prefs["purchase"]["currency_id"] \
                    if "currency_id" in self.user_pref.prefs["purchase"] else None
                initial["dt"] = datetime.datetime.strptime(self.user_pref.prefs["purchase"]["date"], "%Y-%m-%d").date() \
                    if "date" in self.user_pref.prefs["purchase"] else None
        else:
            self.user_pref = None
        kwargs["initial"] = initial
        if "data" in kwargs:
            kwargs["data"] = kwargs["data"].copy()
            kwargs["data"]["food"] = kwargs["data"]["food-id"]
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<h4>Food Purchases</h4> <h6>Please enter a food purchase:</h6>"),
            Div(
                Div(Field("kind", ), css_class="col", ),
                Div(Field("store_name", autofocus="true"), css_class="col"),
                Div(Field("pcs"), css_class="col"),
                css_class="row",
            ),
            Field("food", placeholder="Type food name...", id="food-select", css_class="typeahead autocomplete-select",
                  autocomplete="off", data_url=reverse("food-list", ("v1",)), data_set="results", data_id="id",
                  data_text="description", data_query="search", data_max_results="50"),
            Field("description", placeholder="Optional description..."),
            Div(
                Div(Field("amount"), css_class="col"),
                Div(Field("unit"), css_class="col"),
                css_class="row",
            ),
            Div(
                Div(Field("cost"), css_class="col"),
                Div(Field("currency"), css_class="col"),
                Div(Field("dt"), css_class="col"),
                css_class="row",
            ),
            ButtonHolder(
                Submit("Save", "Log Purchase", css_class="btn-block")
            )
        )

    def is_valid(self):
        valid = super().is_valid()
        if valid and self.user_pref:
            FoodUsageCounter.add_count(self.cleaned_data["food"].id, self.user_pref.owner)
            if "purchase" not in self.user_pref.prefs:
                self.user_pref.prefs["purchase"] = {}
            self.user_pref.prefs["purchase"]["currency_id"] = self.cleaned_data["currency"].id
            self.user_pref.prefs["purchase"]["store"] = self.cleaned_data["store_name"]
            self.user_pref.prefs["purchase"]["unit_id"] = self.cleaned_data["unit"].id
            self.user_pref.prefs["purchase"]["date"] = datetime.datetime.strftime(self.cleaned_data["dt"], '%Y-%m-%d')
            self.user_pref.save()
        return valid
