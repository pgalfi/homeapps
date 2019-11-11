from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from foodtrack.forms import FoodTrackAuthForm, FoodTrackPasswordChangeForm, FoodPurchaseForm, \
    FoodPurchaseItemFilterForm, FoodPurchasesSummaryFilterForm, FoodPurchasesSummaryOptionsForm
from foodtrack.models import PurchaseItem, Currency, FoodLogEntry
from foodtrack.services.data_queries import QueryFoodPurchaseSummarizer
from foodtrack.view_mixins import PreferenceViewMixin, FormFilteredListView, OptionsFormMixin


class FoodTrackLoginView(LoginView):
    template_name = "account/login.html"
    form_class = FoodTrackAuthForm

    def get_redirect_url(self):
        url = super().get_redirect_url()
        return url or reverse_lazy("foodtrack-index")


class Index(LoginRequiredMixin, TemplateView):
    template_name = "layout.html"
    login_url = reverse_lazy("foodtrack-login")


class FoodTrackPasswordView(PasswordChangeView):
    template_name = "account/password_change_form.html"
    form_class = FoodTrackPasswordChangeForm


class FoodLogEntryCreate(LoginRequiredMixin, PreferenceViewMixin, CreateView):
    model = FoodLogEntry


class FoodPurchaseCreate(LoginRequiredMixin, PreferenceViewMixin, CreateView):
    model = PurchaseItem
    form_class = FoodPurchaseForm
    template_name = "food-purchase.html"
    success_url = reverse_lazy("foodtrack-purchase")
    login_url = reverse_lazy("foodtrack-login")


class FoodPurchaseUpdate(LoginRequiredMixin, PreferenceViewMixin, UpdateView):
    model = PurchaseItem
    form_class = FoodPurchaseForm
    template_name = "food-purchase.html"
    success_url = reverse_lazy("foodtrack-purchase-list")
    login_url = reverse_lazy("foodtrack-login")


class FoodPurchaseDelete(LoginRequiredMixin, DeleteView):
    model = PurchaseItem
    success_url = reverse_lazy("foodtrack-purchase-list")
    login_url = reverse_lazy("foodtrack-login")

    def get(self, request, *args, **kwargs):
        # skip confirmation logic provided by GET request and convert it to a delete
        return self.post(request, *args, **kwargs)


class FoodPurchaseListForm(LoginRequiredMixin, FormFilteredListView):
    template_name = "food-purchase-list.html"
    form_class = FoodPurchaseItemFilterForm
    queryset = PurchaseItem.objects.all()
    ordering = "-dt"
    paginate_by = 5


class FoodPurchasesSummary(LoginRequiredMixin, OptionsFormMixin, FormFilteredListView):
    template_name = "food-purchase-summary.html"
    form_class = FoodPurchasesSummaryFilterForm
    options_form_class = FoodPurchasesSummaryOptionsForm
    queryset = PurchaseItem.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        self.kwargs["options_form"] = self.get_options_form()
        options_form: Form = self.kwargs["options_form"]
        options_form.full_clean()
        if "summary_type" not in options_form.cleaned_data:
            return PurchaseItem.objects.none()
        return QueryFoodPurchaseSummarizer(qs, int(options_form.cleaned_data["summary_type"])).apply()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        options_form: Form = self.kwargs["options_form"]
        if "currency_id" in options_form.cleaned_data:
            context_data["currency"] = Currency.objects.get(pk=options_form.cleaned_data["currency_id"])
        return context_data

