from rest_framework import serializers

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




