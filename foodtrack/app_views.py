from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django_filters.views import FilterView

from foodtrack.app_forms import FoodTrackAuthForm, FoodTrackPasswordChangeForm, FoodPurchaseForm
from foodtrack.filters import FoodPurchaseItemFilter
from foodtrack.models import PurchaseItem
from foodtrack.services.user_prefs import load_model_preference


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


class FoodPurchase(LoginRequiredMixin, CreateView):
    model = PurchaseItem
    form_class = FoodPurchaseForm
    template_name = "food-purchase.html"
    success_url = reverse_lazy("foodtrack-purchase")
    login_url = reverse_lazy("foodtrack-login")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = load_model_preference(PurchaseItem, self.request.user.id)
        if "data" in kwargs:
            kwargs["data"] = kwargs["data"].copy()
            kwargs["data"]["owner"] = self.request.user.id
        return kwargs


class FoodPurchaseList(LoginRequiredMixin, FilterView):
    template_name = "food-purchase-list.html"
    paginate_by = 10
    filterset_class = FoodPurchaseItemFilter
