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
        fields = ('__all__')

class FoodRequestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    clorie = serializers.IntegerField()
    potion = serializers.IntegerField()
    level = serializers.IntegerField()
    star_level = serializers.IntegerField()
    prepare = serializers.CharField()
    youtube_url = serializers.CharField(max_length=500)
    category_id = serializers.UUIDField()
    class Meta:
        model = Food
        fields = ('name','clorie','potion','level','star_level','prepare','youtube_url','category_id')

class FoodResponseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    clorie = serializers.IntegerField()
    potion = serializers.IntegerField()
    level = serializers.IntegerField()
    star_level = serializers.IntegerField()
    prepare = serializers.CharField()
    youtube_url = serializers.CharField(max_length=500)
    category = CategorySerializer(many=False)
    class Meta:
        model = Food
        fields = ('__all__')

class ReviewRequestSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    food_id = serializers.UUIDField()
    class Meta:
        model = Review
        fields = ('content', 'food_id')

class ReviewResponseSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    food = FoodResponseSerializer(many=False)
    class Meta:
        model = Review
        fields = ('__all__')

class FoodIngredientRequestSerializer(serializers.ModelSerializer):
    food_id = serializers.UUIDField()
    ingredient_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    class Meta:
        model = FoodIngredient
        fields = ('food_id', 'ingredient_id', 'quantity')

class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Ingredient
        fields = ('__all__')


class FoodIngredientResponseSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    food = FoodResponseSerializer(many=False)
    ingredient = IngredientSerializer(many=False)
    class Meta:
        model = FoodIngredient
        fields = ('__all__')
        depth = 1

class UserFavoriteFoodRequestSerializer(serializers.ModelSerializer):
    food_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    class Meta:
        model = UserFavoriteFood
        fields = ('food_id','user_id')

class UserFavoriteFoodResponseSerializer(serializers.ModelSerializer):
    food = FoodResponseSerializer(many=False)
    user = UserSerializer(many=False)
    class Meta:
        model = UserFavoriteFood
        fields = ('__all__')