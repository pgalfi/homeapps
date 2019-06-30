from rest_framework import serializers

from foodtrack.models import *


class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ('id', 'name', 'unit')


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = ('id', 'name')


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id', 'description')


class FoodNutrientSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodNutrientSource
        fields = ('id', 'description')


class FoodNutrientDerivationSerializer(serializers.ModelSerializer):
    source = FoodNutrientSourceSerializer(many=False)

    class Meta:
        model = FoodNutrientDerivation
        fields = ('id', 'description', 'source')


class FoodNutrientSerializer(serializers.ModelSerializer):
    nutrient = NutrientSerializer(many=False, read_only=True)

    class Meta:
        model = FoodNutrient
        fields = ('id', 'nutrient', 'amount')


class FoodPortionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodPortion
        fields = ('id', 'food', 'amount', 'unit', 'description', 'modifier', 'gram_weight')


class FoodSerializer(serializers.ModelSerializer):
    category = FoodCategorySerializer(many=False)

    class Meta:
        model = Food
        fields = ('id', 'data_type', 'description', 'pub_date', 'category')


class FoodDetailSerializer(serializers.ModelSerializer):
    category = FoodCategorySerializer(many=False)
    nutrients = FoodNutrientSerializer(many=True)

    class Meta:
        model = Food
        fields = ('id', 'data_type', 'description', 'pub_date', 'category', 'nutrients')


class FoodLogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLogCategory
        fields = ('id', 'name')


class FoodLogEntryNutrientSerializer(serializers.ModelSerializer):
    nutrient = NutrientSerializer(many=False, read_only=True)

    class Meta:
        model = FoodLogEntryNutrient
        fields = ('amount', 'nutrient')


class FoodLogEntrySerializer(serializers.ModelSerializer):
    category_name = serializers.SlugField(source="category.name", read_only=True)
    food_desc = serializers.SlugField(source="food.description", read_only=True)
    portion_name = serializers.SlugField(source="portion.name", read_only=True)
    nutrients = FoodLogEntryNutrientSerializer(many=True, read_only=True)

    class Meta:
        model = FoodLogEntry
        fields = ('id', 'dt', 'category', 'category_name', 'food',
                  'food_desc', 'amount', 'portion', 'portion_name',
                  'nutrients')
