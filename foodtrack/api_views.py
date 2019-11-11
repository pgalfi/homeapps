import datetime

from django.db.models import Q
from rest_framework import viewsets, permissions, mixins
from rest_framework.filters import OrderingFilter, SearchFilter

import foodtrack.services.data_events
from foodtrack.api_filters import FieldFilter
from foodtrack.serializers import *
from foodtrack.services import nutrients
from foodtrack.services.data_union import QuerySetUnion


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class UsageOrderingFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            ordering = ["-usage__count", "-data_type"] + list(ordering)
        else:
            ordering = ["-usage__count", "-data_type"]
        return queryset.order_by(*ordering)


class NutrientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer

    def get_queryset(self):
        return Nutrient.objects.all().order_by("-usage__count", "name")


class MeasureUnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer


class FoodCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer


class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (FieldFilter, SearchFilter, UsageOrderingFilter)
    field_names = ('category', 'data_type')
    search_fields = ('description',)
    ordering_fields = ('description',)
    ordering = ('description',)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FoodDetailSerializer
        return FoodSerializer

    def get_queryset(self):
        # Based on the type of serializer that will be used provide querysets that load all needed data efficiently
        if self.action == "list":
            return Food.objects.all().select_related("category")
        if self.action == "retrieve":
            return Food.objects.all().select_related("category").prefetch_related("nutrients", "nutrients__nutrient")
        return Food.objects.all()


class FoodLogCategoryViewSet(viewsets.ModelViewSet):
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
        log_entry: FoodLogEntry = serializer.save(user=self.request.user)
        nutrients.build_nutrients(log_entry)
        nutrients.generate_nutrient_targets(self.request.user)
        foodtrack.services.data_events.add_food_usage_count(log_entry.food, self.request.user)


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


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        recipe = serializer.save(owner=self.request.user)
        nutrients.compute_nutrients(recipe)

    def perform_update(self, serializer):
        recipe = serializer.save()
        nutrients.compute_nutrients(recipe)


class RecipeComponentViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeComponentSerializer
    queryset = RecipeComponent.objects.all()


class FoodAndRecipeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FoodAndRecipeFacadeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('description', )
    ordering_fields = ('description', )

    def get_queryset(self) -> QuerySetUnion:
        return QuerySetUnion(Food.objects.values_list("id", "description", "data_type"),
                             Recipe.objects.values_list("id", "name", "data_type"))
