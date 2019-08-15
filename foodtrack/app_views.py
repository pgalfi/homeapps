from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, ModelFormMixin

from foodtrack.app_forms import FoodTrackAuthForm, FoodTrackPasswordChangeForm, FoodPurchaseForm
from foodtrack.models import PurchaseItem, UserPreference


class UserPreferencesMixin(ModelFormMixin):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs["initial"]["user_preference"], created = UserPreference.objects.get_or_create(
                owner=self.request.user)
        return kwargs


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


class FoodPurchaseView(LoginRequiredMixin, UserPreferencesMixin, CreateView):
    model = PurchaseItem
    form_class = FoodPurchaseForm
    template_name = "food-purchase.html"
    success_url = reverse_lazy("foodtrack-purchase")
    login_url = reverse_lazy("foodtrack-login")
