from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormMixin

from foodtrack.app_forms import FoodTrackAuthForm, FoodTrackPasswordChangeForm, FoodPurchaseForm, \
    FoodPurchaseItemFilterForm
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


class FoodPurchaseList(LoginRequiredMixin, FormMixin, ListView):
    template_name = "food-purchase-list.html"
    paginate_by = 10
    form_class = FoodPurchaseItemFilterForm

    def get_queryset(self):
        qs = PurchaseItem.objects.filter(owner=self.request.user).order_by("dt")

        return qs





