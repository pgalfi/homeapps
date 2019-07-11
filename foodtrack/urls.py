from django.urls import path, include
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from foodtrack import views, gql_schema

router = DefaultRouter()
router.register('nutrients', views.NutrientViewSet)
router.register('measures', views.MeasureUnitViewSet)
router.register('foodcategories', views.FoodCategoryViewSet)
router.register('food', views.FoodViewSet)
router.register('foodlogcategories', views.FoodLogCategoryViewSet)
router.register('foodlogentries', views.FoodLogEntryViewSet)
router.register('currency', views.CurrencyViewSet)
router.register('purchaseitems', views.PurchaseItemViewSet)
router.register('nutritionprofiles', views.NutritionProfileViewSet)
router.register('nutritionprofiletarget', views.NutritionProfileTargetViewSet)
router.register('usernutrition', views.UserNutritionViewSet)
router.register('recipes',views.RecipeViewSet)
router.register('recipecomponents', views.RecipeComponentViewSet)
router.register('foodusage', views.FoodUsageCounterViewSet)
router.register('nutrientusage', views.NutrientUsageCounterViewSet)

urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=gql_schema.schema)),
    path('', include(router.urls)),

]