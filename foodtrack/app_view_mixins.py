import datetime

from django.forms import Form
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import ModelFormMixin, FormMixin

from foodtrack.services.user_prefs import load_form_preference, save_form_preference


class PreferenceViewMixin(ModelFormMixin, View):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "GET":
            kwargs["initial"] = load_form_preference(self.form_class, self.request.user.id)
        if "data" in kwargs:
            kwargs["data"] = kwargs["data"].copy()
            kwargs["data"]["owner"] = self.request.user.id
        return kwargs

    def form_valid(self, form: Form):
        response = super().form_valid(form)
        save_form_preference(form.__class__, form.cleaned_data, self.request.user.id)
        return response


class FilteredListView(FormMixin, ListView):

    empty_values = (None, '')

    def get_empty_values(self):
        return self.empty_values

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs().copy()
        kwargs.update({
            "data": self.request.GET
        })
        return kwargs

    def get_queryset(self):
        qs = super().get_queryset()
        self.kwargs["form"] = self.get_form()
        form: Form = self.kwargs["form"]
        form.full_clean()
        for cleaned_field, cleaned_data in form.cleaned_data.items():
            if cleaned_data in self.get_empty_values(): continue
            if isinstance(cleaned_data, datetime.date) or isinstance(cleaned_data, datetime.datetime):
                if "_start" in cleaned_field: qs = qs.filter(**{cleaned_field.replace("_start","")+"__gte": cleaned_data})
                elif "_end" in cleaned_field: qs = qs.filter(**{cleaned_field.replace("_end","")+"__lte": cleaned_data})
                else: qs = qs.filter(**{cleaned_field: cleaned_data})
            else:
                qs = qs.filter(**{cleaned_field: cleaned_data})
        return qs


