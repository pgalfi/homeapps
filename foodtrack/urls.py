from django.urls import path, include
from rest_framework.routers import DefaultRouter

from foodtrack import views

router = DefaultRouter()
router.register('nutrients', views.NutrientViewSet)
router.register('measures', views.MeasureUnitViewSet)
router.register('foodcategories', views.FoodCategoryViewSet)
router.register('food', views.FoodViewSet)
router.register('foodlogcategories', views.FoodLogCategoryViewSet)
router.register('foodlogentries', views.FoodLogEntryViewSet)
router.register('currency', views.CurrencyViewSet)
router.register('purchaseitems', views.PurchaseItemViewSet)


urlpatterns = [
    path('', include(router.urls)),

]