from django.urls import include, path
from rest_framework.routers import DefaultRouter

from housing import views

router = DefaultRouter()
router.register("houses", views.HouseProspectViewSet)

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('api/', include(router.urls)),
]