from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Hidden, HTML, Field, Div
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from rest_framework.reverse import reverse

from foodtrack.models import PurchaseItem


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

    def __init__(self, *args, **kwargs):
        if "data" in kwargs and "food-id" in kwargs["data"]:
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


class FoodPurchaseItemFilterForm(forms.Form):
    food = forms.CharField(required=False)
    store_name = forms.CharField(required=False)
    date_start = forms.DateField(required=False, widget=forms.TextInput(attrs={"type": "date"}))
    date_end = forms.DateField(required=False, widget=forms.TextInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        if "data" in kwargs and "food-id" in kwargs["data"]:
            kwargs["data"]["food"] = kwargs["data"]["food-id"]

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<h4>My Food Purchases</h4>"),
            Field("food", placeholder="Type food name...", id="food-select", autocomplete="off",
                  css_class="typeahead autocomplete-select form-control-sm", data_url=reverse("food-list", ("v1",)),
                  data_set="results", data_id="id", data_text="description", data_query="search", data_max_results="50"),
            Div(
                Div(Field("store_name", autofocus="true", css_class="form-control-sm"), css_class="col"),
                Div(Field("date_start", css_class="form-control-sm"), css_class="col"),
                Div(Field("date_end", css_class="form-control-sm"), css_class="col"),
                css_class="row",
            ),
        )


