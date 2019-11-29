import datetime

from django.db.models import Q
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import foodtrack.services.data_events
from foodtrack.api.filters import FieldFiltering
from foodtrack.api.serializers import *
from foodtrack.api.view_mixins import PerformanceCheckMixin
from foodtrack.services import nutrients
from foodtrack.services.data_proxies import create_usage_proxy
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
    filter_backends = (FieldFiltering, UsageOrderingFilter)
    filter_fields = [{"name": "category"},
                     {"name": "data_type", "label": "Data Type"},
                     {"name": "description", "lookup": "icontains"}]
    ordering_fields = ('description',)
    ordering = ('description',)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FoodDetailSerializer
        return FoodSerializer

    def get_queryset(self):
        FoodProxy = create_usage_proxy(self.request.user.id, Food)
        qs = FoodProxy.objects.all()

        # Based on the type of serializer that will be used provide querysets that load all needed data efficiently
        if self.action == "list":
            return qs.select_related("category")
        if self.action == "retrieve":
            return qs.select_related("category").prefetch_related("nutrients", "nutrients__nutrient")
        return qs


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


class FoodAndRecipeViewSet(mixins.ListModelMixin, PerformanceCheckMixin, viewsets.GenericViewSet):
    serializer_class = FoodAndRecipeFacadeSerializer
    filter_backends = (FieldFiltering, UsageOrderingFilter)
    filter_fields = [{"name": "description", "label": "Name", "lookup": "icontains"},
                     {"name": "data_type", "label": "Data Type"}]
    ordering_fields = ('description',)
    ordering = ('description',)

    def get_queryset(self) -> QuerySetUnion:
        FoodProxy = create_usage_proxy(self.request.user.id, Food)
        RecipeProxy = create_usage_proxy(self.request.user.id, Recipe)

        return QuerySetUnion(FoodProxy.objects.values_list("id", "description", "data_type", "usage__count"),
                             RecipeProxy.objects.values_list("id", "name", "data_type", "usage__count"))


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
