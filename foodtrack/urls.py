from django.urls import path, include
from rest_framework.routers import DefaultRouter

from foodtrack import views

router = DefaultRouter()
router.register('nutrients', views.NutrientViewSet)
router.register('measures', views.MeasureUnitViewSet)
router.register('foodcategories', views.FoodCategoryViewSet)
router.register('food', views.FoodViewSet)

urlpatterns = [
    path('', include(router.urls)),

]