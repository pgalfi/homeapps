from django.contrib.auth.views import logout_then_login
from django.urls import path, include, re_path, reverse_lazy
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from foodtrack import views
from foodtrack.api import views as api_views

router = DefaultRouter()
router.register('nutrients', api_views.NutrientViewSet)
router.register('measures', api_views.MeasureUnitViewSet)
router.register('foodcategories', api_views.FoodCategoryViewSet)
router.register('food', api_views.FoodViewSet, basename="food")
router.register('foodlogcategories', api_views.FoodLogCategoryViewSet)
router.register('foodlogentries', api_views.FoodLogEntryViewSet)
router.register('currency', api_views.CurrencyViewSet)
router.register('purchaseitems', api_views.PurchaseItemViewSet)
router.register('nutritionprofiles', api_views.NutritionProfileViewSet)
router.register('nutritionprofiletarget', api_views.NutritionProfileTargetViewSet)
router.register('usernutrition', api_views.UserNutritionViewSet)
router.register('recipes', api_views.RecipeViewSet)
router.register('foodandrecipe', api_views.FoodAndRecipeViewSet, basename="foodandrecipe")
router.register('recipecomponents', api_views.RecipeComponentViewSet)
# print(router.urls)

urlpatterns = [
    # APIs
    re_path('(?P<version>(v1))/api-token-auth/', obtain_auth_token),
    re_path('(?P<version>(v1))/user/password', api_views.ChangePasswordView.as_view(), name="password"),
    re_path('(?P<version>(v1))/', include(router.urls)),

    path('/', app_views.Index.as_view(), name='foodtrack-index'),
    path('index/', app_views.Index.as_view(), name='foodtrack-index'),

    path('account/login/', views.FoodTrackLoginView.as_view(), name='foodtrack-login'),
    path('account/password/', views.FoodTrackPasswordView.as_view(), name='foodtrack-password'),
    path('account/logout/', logout_then_login, {"login_url": reverse_lazy("foodtrack-login")}, name="foodtrack-logout"),

    path('purchase/new', views.FoodPurchaseCreate.as_view(), name='foodtrack-purchase'),
    path('purchase/list', views.FoodPurchaseListForm.as_view(), name='foodtrack-purchase-list'),
    path('purchase/summary', views.FoodPurchasesSummary.as_view(), name='foodtrack-purchase-summary'),
    path('purchase/update/<int:pk>/', views.FoodPurchaseUpdate.as_view(), name='foodtrack-purchase-update'),
    path('purchase/delete/<int:pk>/', views.FoodPurchaseDelete.as_view(), name='foodtrack-purchase-delete'),

    path('foodlog/new', views.NewFoodLogEntry.as_view(), name='foodtrack-log-newentry'),
]