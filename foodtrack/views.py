import datetime

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from foodtrack.serializers import *


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
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('category', 'data_type')
    search_fields = ('description',)
    ordering_fields = ('description',)
    ordering = ('description',)

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
        return FoodLogCategory.objects.filter(Q(owner__isnull=True) | Q(owner=self.request.user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FoodLogEntryViewSet(viewsets.ModelViewSet):
    serializer_class = FoodLogEntrySerializer
    queryset = FoodLogEntry.objects.all()

    def perform_create(self, serializer):
        log_entry = serializer.save(user=self.request.user)
        FoodLogEntryNutrient.build_nutrients(log_entry)
        NutrientTargets.generate(self.request.user)


class CurrencyViewSet(viewsets.ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()

    def perform_create(self, serializer):
        serializer.save(rate_date=datetime.datetime.now())


class PurchaseItemViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseItemSerializer
    queryset = PurchaseItem.objects.all()

    def perform_create(self, serializer):
        serializer.save(dt=datetime.datetime.now())


class NutritionProfileViewSet(viewsets.ModelViewSet):
    serializer_class = NutritionProfileSerializer
    queryset = NutritionProfile.objects.all()


class NutritionProfileTargetViewSet(viewsets.ModelViewSet):
    serializer_class = NutritionProfileTargetSerializer
    queryset = NutritionProfileTarget.objects.all()


class UserNutritionViewSet(viewsets.ModelViewSet):
    serializer_class = UserNutritionSerializer
    queryset = UserNutrition.objects.all()
