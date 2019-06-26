from django.urls import path

from foodtrack import views

urlpatterns = [
    path('api/foods', views.FoodListCreate.as_view()),

]