from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Food, Image, User, Category, Ingredient


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Category
        fields = ('__all__')


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = ('__all__')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('__all__')


class DetailIngredientInFoodSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField()
    quantity = serializers.CharField()


class FoodSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    cover_image_id = serializers.IntegerField(allow_null=True)
    detail_ingredients = DetailIngredientInFoodSerializer(many=True)

    class Meta:
        model = Food
        exclude = ['category', 'cover_image']

class FoodHomeSerializer(serializers.ModelSerializer):
    cover_image = SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Food
        fields = ('id', 'name', 'cover_image', 'star_level')

