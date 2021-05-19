from rest_framework import fields, serializers

from .models import User, Food, UserFavoriteFood, Ingredient, FoodIngredient, Review, Category

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=50)
    user_name = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=20)
    class Meta:
        model = User
        fields = ('id','full_name', 'user_name', 'email', 'password')

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    class Meta:
        model = User
        fields = ('email', 'password')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    class Meta:
        model = Category
        fields = ('id','name')

class FoodSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    calorie = serializers.IntegerField()
    potion = serializers.IntegerField()
    level = serializers.IntegerField()
    star_level = serializers.IntegerField()
    prepare = serializers.CharField()
    youtube_url = serializers.CharField(max_length=500)
    category_id = serializers.UUIDField()
    class Meta:
        model = Food
        fields = ('__all__')

class ReviewSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    food_id = serializers.UUIDField()
    class Meta:
        model = Review
        fields = ('__all__')

class FoodIngredientSerializer(serializers.ModelSerializer):
    food_id = serializers.UUIDField()
    ingredient_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    class Meta:
        model = FoodIngredient
        fields = ('__all__')

class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Ingredient
        fields = ('__all__')

class UserFavoriteFoodSerializer(serializers.ModelSerializer):
    food_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    class Meta:
        model = FoodIngredient
        fields = ('__all__')