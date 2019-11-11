from rest_framework import serializers

from foodtrack.models import *


class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ('id', 'name', 'unit')


class MeasureUnitSerializer(serializers.ModelSerializer):
    # link_id = serializers.HyperlinkedIdentityField(view_name='measureunit-detail')
    class Meta:
        model = MeasureUnit
        fields = ('id', 'name', 'kind')


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
    detail = serializers.HyperlinkedIdentityField(view_name='food-detail')

    class Meta:
        model = Food
        fields = ('id', 'detail', 'data_type', 'description', 'pub_date', 'category')


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
    alt_food_name = serializers.SlugField(source="alt_food.name", read_only=True)

    class Meta:
        model = FoodLogEntry
        fields = ('id', 'dt', 'category', 'category_name', 'food',
                  'food_desc', 'alt_food', 'alt_food_name', 'amount',
                  'portion', 'portion_name', 'nutrients')


class CurrencySerializer(serializers.ModelSerializer):
    rate_date = serializers.ReadOnlyField()

    class Meta:
        model = Currency
        fields = ('id', 'name', 'long_name', 'rate', 'rate_date')


class PurchaseItemSerializer(serializers.ModelSerializer):
    dt = serializers.ReadOnlyField()
    unit_name = serializers.ReadOnlyField(source='unit.name')
    currency_name = serializers.ReadOnlyField(source='currency.name')
    food = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Food.objects.all(),
                                              style={"base_template": "input.html"})

    class Meta:
        model = PurchaseItem
        fields = ('id', 'kind', 'food', 'description', 'pcs', 'amount', 'unit', 'unit_name',
                  'cost', 'currency', 'currency_name', 'dt')


class NutritionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionProfile
        fields = ('id', 'name', 'kind')


class NutritionProfileTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionProfileTarget
        fields = ('id', 'profile', 'nutrient', 'amount', 'kind', 'notes')


class UserNutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNutrition
        fields = ('id', 'user', 'profile')


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'serving_amount', 'prep_time', 'directions')


class RecipeComponentSerializer(serializers.ModelSerializer):
    link_id = serializers.HyperlinkedIdentityField(view_name='recipecomponent-detail')
    recipe_name = serializers.ReadOnlyField(source="recipe.name")
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(),
                                              style={"base_template": "input.html"})
    food_name = serializers.ReadOnlyField(source="food.description")
    portion_name = serializers.ReadOnlyField(source='portion.name')


    class Meta:
        model = RecipeComponent
        fields = ('link_id', 'id', 'recipe', 'recipe_name', 'food', 'food_name',
                  'amount', 'portion', 'portion_name')


class FoodAndRecipeFacadeSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return_data = {
            "id": instance[0],
            "name": instance[1],
            "data_type": instance[2],
        }
        return return_data

    def to_internal_value(self, data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError




