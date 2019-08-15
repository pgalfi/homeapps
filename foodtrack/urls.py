from django.contrib.auth.views import logout_then_login
from django.urls import path, include, re_path, reverse_lazy
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from foodtrack import api_views, gql_schema, app_views

router = DefaultRouter()
router.register('nutrients', api_views.NutrientViewSet)
router.register('measures', api_views.MeasureUnitViewSet)
router.register('foodcategories', api_views.FoodCategoryViewSet)
router.register('food', api_views.FoodViewSet)
router.register('foodlogcategories', api_views.FoodLogCategoryViewSet)
router.register('foodlogentries', api_views.FoodLogEntryViewSet)
router.register('currency', api_views.CurrencyViewSet)
router.register('purchaseitems', api_views.PurchaseItemViewSet)
router.register('nutritionprofiles', api_views.NutritionProfileViewSet)
router.register('nutritionprofiletarget', api_views.NutritionProfileTargetViewSet)
router.register('usernutrition', api_views.UserNutritionViewSet)
router.register('recipes', api_views.RecipeViewSet)
router.register('recipecomponents', api_views.RecipeComponentViewSet)

urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=gql_schema.schema)),
    re_path('(?P<version>(v1))/', include(router.urls)),
    path('', app_views.Index.as_view(), name='foodtrack-index'),
    path('index/', app_views.Index.as_view(), name='foodtrack-index'),
    path('account/login/', app_views.FoodTrackLoginView.as_view(), name='foodtrack-login'),
    path('account/password/', app_views.FoodTrackPasswordView.as_view(), name='foodtrack-password'),
    path('account/logout/', logout_then_login, {"login_url": reverse_lazy("foodtrack-login")}, name="foodtrack-logout"),
    path('purchase/', app_views.FoodPurchaseView.as_view(), name='foodtrack-purchase'),
]