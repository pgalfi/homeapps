import string

from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from foodtrack.models import Nutrient, MeasureUnit, FoodCategory, Food, FoodLogCategory, FoodLogEntry, \
    FoodLogEntryNutrient
from foodtrack.serializers import NutrientSerializer, MeasureUnitSerializer, FoodCategorySerializer, FoodSerializer, \
    FoodDetailSerializer, FoodLogCategorySerializer, FoodLogEntrySerializer


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


class FoodLogCategoryViewSet(viewsets.ModelViewSet):

    class IsOwner(permissions.BasePermission):

        def has_object_permission(self, request, view, obj):
            return obj.owner == request.user

    serializer_class = FoodLogCategorySerializer
    queryset = FoodLogCategory.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return FoodLogCategory.objects.filter(Q(owner__isnull=True)|Q(owner=self.request.user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FoodLogEntryViewSet(viewsets.ModelViewSet):

    serializer_class = FoodLogEntrySerializer
    queryset = FoodLogEntry.objects.all()

    def perform_create(self, serializer):
        log_entry = serializer.save(user=self.request.user)
        FoodLogEntryNutrient.build_nutrients(log_entry)

