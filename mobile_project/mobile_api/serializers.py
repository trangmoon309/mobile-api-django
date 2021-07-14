from rest_framework import serializers

from .models import User, Category, Ingredient


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
