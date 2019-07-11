import graphene
from django_filters import FilterSet, Filter, CharFilter
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from foodtrack.models import *


class NutrientType(DjangoObjectType):
    class Meta:
        model = Nutrient


class MeasureUnitType(DjangoObjectType):
    class Meta:
        model = MeasureUnit


class FoodCategoryType(DjangoObjectType):
    class Meta:
        model = FoodCategory


class FoodNutrientType(DjangoObjectType):
    class Meta:
        model = FoodNutrient
        filter_fields = {
            'amount': ["gt", "exact", "lt"]
        }
        interfaces = (graphene.relay.Node,)


class FoodNode(graphene.Node):
    class Meta:
        name = 'FoodNode'

    @classmethod
    def to_global_id(cls, type, id):
        return id


class FoodType(DjangoObjectType):
    nutrients = DjangoFilterConnectionField(FoodNutrientType)

    class Meta:
        model = Food
        interfaces = (FoodNode,)


class FoodNutrientSourceType(DjangoObjectType):
    class Meta:
        model = FoodNutrientSource


class FoodNutrientDerivationType(DjangoObjectType):
    class Meta:
        model = FoodNutrientDerivation


class FoodPortionType(DjangoObjectType):
    class Meta:
        model = FoodPortion


class WordFilter(Filter):
    def filter(self, qs, value):
        words = value.split()
        for word in words:
            qs = qs.filter(**{self.field_name + "__icontains": word})
        return qs


class FoodTypeFilter(FilterSet):
    description = WordFilter()
    data_type = CharFilter()
    fields = ['data_type', 'description']


class Query(ObjectType):
    food = graphene.Field(FoodType, id=graphene.Int())
    foods = DjangoFilterConnectionField(FoodType, filterset_class=FoodTypeFilter)

    @staticmethod
    def resolve_food(parent, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Food.objects.get(pk=id)
        return None


schema = graphene.Schema(query=Query)
