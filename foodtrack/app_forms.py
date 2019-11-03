from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Hidden, HTML, Field, Div
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.urls import reverse_lazy
from rest_framework.reverse import reverse

from foodtrack.models import PurchaseItem


class FoodTrackAuthForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.helper = FormHelper()
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
    food_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    description = forms.CharField(required=False)
    pcs = forms.IntegerField(min_value=1, initial=1)
    amount = forms.FloatField(min_value=0.0001)
    cost = forms.FloatField(min_value=0.0001)

    class Meta:
        model = PurchaseItem
        fields = ["kind", "food", "description", "pcs", "amount", "unit", "cost", "currency", "store_name", "dt",
                  "owner"]
        widgets = {
            "food": forms.TextInput,
            "dt": forms.TextInput(
                attrs={"type": "date"}
            ),
        }
        labels = {
            "dt": "Purchase date"
        }

    class prefs:
        fields = ["dt", "unit", "currency", "store_name"]

    def __init__(self, *args, **kwargs):
        if "data" in kwargs and "food_id" in kwargs["data"]:
            kwargs["data"]["food"] = kwargs["data"]["food_id"]

        if kwargs["instance"]:
            if "initial" not in kwargs: kwargs["initial"] = {}
            kwargs["initial"]["food"] = kwargs["instance"].food.description
            kwargs["initial"]["food_id"] = kwargs["instance"].food.id
            kwargs["initial"]["dt"] = kwargs["instance"].dt.strftime("%Y-%m-%d")

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<h4>Food Purchases</h4> <h6>Please enter food purchase data:</h6>"),
            Div(
                Div(Field("kind", ), css_class="col", ),
                Div(Field("store_name", autofocus="true"), css_class="col"),
                Div(Field("pcs"), css_class="col"),
                css_class="row",
            ),
            Field("food_id"),
            Field("food", placeholder="Type food name...", id="food-select", css_class="typeahead autocomplete-select",
                  autocomplete="off", data_url=reverse("food-list", args=["v1"]), data_set="results", data_id="id",
                  data_text="description", data_query="search", data_max_results="50", data_set_name="food_id"),
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
                Submit("Save", "Save", css_class="btn-block")
            )
        )


class FoodPurchaseItemFilterForm(forms.Form):
    food_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    food = forms.CharField(required=False,
                           widget=forms.TextInput(
                               attrs={
                                   "placeholder": "Type food name...",
                                   "autocomplete": "off",
                                   "class": "typeahead autocomplete-select form-control-sm",
                                   "data-url": reverse_lazy("food-list", args=["v1"]),
                                   "data-set": "results",
                                   "data-id": "id",
                                   "data-text": "description",
                                   "data-query": "search",
                                   "data-max-results": "50",
                                   "data-set-name": "food_id"
                               }
                           ))

    store_name = forms.CharField(required=False)
    dt_start = forms.DateField(required=False, widget=forms.TextInput(attrs={"type": "date"}), label="Date start")
    dt_end = forms.DateField(required=False, widget=forms.TextInput(attrs={"type": "date"}), label="Date end")


class FoodPurchasesSummaryFilterForm(forms.Form):
    store_name = forms.CharField(required=True, empty_value=None)
    dt_start = forms.DateField(required=True, widget=forms.TextInput(attrs={"type": "date"}), label="Date start")
    dt_end = forms.DateField(required=True, widget=forms.TextInput(attrs={"type": "date"}), label="Date end")
