from django.forms import Form
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import ModelFormMixin, FormMixin

from foodtrack.services.data_queries import QuerySetFormFilter
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


class FormFilteredListView(FormMixin, ListView):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs().copy()
        kwargs.update({
            "data": self.request.GET
        })
        return kwargs

    def get_queryset(self):
        qs = super().get_queryset()
        self.kwargs["form"] = self.get_form()
        form = self.kwargs["form"]
        return QuerySetFormFilter(qs, form).apply()


class OptionsFormMixin(FormMixin):
    options_form_class = None

    def get_options_form_class(self):
        return self.options_form_class

    def get_options_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_options_form_class()
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        if 'options_form' not in kwargs:
            kwargs['options_form'] = self.get_options_form()
        return super().get_context_data(**kwargs)


