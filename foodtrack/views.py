from rest_framework import generics

from foodtrack.models import Food
from foodtrack.serializers import FoodSerializer


class FoodListCreate(generics.ListCreateAPIView):
    queryset = Food.objects.all()[:200]
    serializer_class = FoodSerializer
