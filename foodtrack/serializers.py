from rest_framework import serializers

from foodtrack.models import Food, Nutrient, MeasureUnit, FoodCategory, FoodNutrientSource, FoodNutrientDerivation, \
    FoodNutrient


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
    source = serializers.ReadOnlyField(source='source.description')
    source_id = serializers.ReadOnlyField(source='source.id')

    class Meta:
        model = FoodNutrientDerivation
        fields = ('id', 'description', 'source_id', 'source')


class FoodNutrientSerializer(serializers.ModelSerializer):
    nutrient = NutrientSerializer(many=False, read_only=True)

    class Meta:
        model = FoodNutrient
        fields = ('id', 'nutrient', 'amount')


class FoodSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.description')
    category_id = serializers.ReadOnlyField(source='category.id')
    # nutrients = FoodNutrientSerializer(many=True)

    class Meta:
        model = Food
        fields = ('id', 'data_type', 'description', 'pub_date', 'category_id', 'category')


class FoodDetailSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.description')
    category_id = serializers.ReadOnlyField(source='category.id')
    nutrients = FoodNutrientSerializer(many=True)

    class Meta:
        model = Food
        fields = ('id', 'data_type', 'description', 'pub_date', 'category_id', 'category', 'nutrients')
