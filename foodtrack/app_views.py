from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from foodtrack.app_forms import FoodTrackAuthForm, FoodTrackPasswordChangeForm, FoodPurchaseForm, \
    FoodPurchaseItemFilterForm, FoodPurchasesSummaryFilterForm
from foodtrack.app_view_mixins import PreferenceViewMixin, FilteredListView
from foodtrack.models import PurchaseItem


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


class FoodPurchaseList(LoginRequiredMixin, FilteredListView):
    template_name = "food-purchase-list.html"
    form_class = FoodPurchaseItemFilterForm
    queryset = PurchaseItem.objects.all()
    ordering = "-dt"
    paginate_by = 5
