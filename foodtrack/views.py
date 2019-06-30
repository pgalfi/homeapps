import string

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from foodtrack.models import Nutrient, MeasureUnit, FoodCategory, Food
from foodtrack.serializers import NutrientSerializer, MeasureUnitSerializer, FoodCategorySerializer, FoodSerializer, \
    FoodDetailSerializer


class NutrientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer


class MeasureUnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer


class FoodCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer


class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()

    def get_queryset(self):
        queryset = Food.objects.all()
        q_name = self.request.query_params.get("name", None)
        q_cat = self.request.query_params.get("cat", None)
        if q_name is not None:
            parts = q_name.translate(str.maketrans('', '', string.punctuation)).split()
            for apart in parts:
                queryset = queryset.filter(description__icontains=apart)
        if q_cat is not None:
            queryset = queryset.filter(category_id=q_cat)
        queryset = queryset.order_by('description')
        return queryset

    def retrieve(self, request, pk=None, **kwargs):
        food = get_object_or_404(Food.objects.all(), pk=pk)
        serializer = FoodDetailSerializer(food)
        return Response(serializer.data)
