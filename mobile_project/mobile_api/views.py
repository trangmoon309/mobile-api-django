from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.decorators import parser_classes


from .models import User, Food, UserFavoriteFood, Ingredient, FoodIngredient, Review, Category
from . import serializers
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render

class UserAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    throttle_scope = "users_app"

    def get(self, request):
        users = User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

class SignUpAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    throttle_scope = "users_app"
    def post(self, request, *args, **kwargs):
        user_data = request.data

        checkExistUserName = User.objects.get(user_name=user_data["user_name"])
        if checkExistUserName:
            return HttpResponse("Username has existed!", status=404)
        else:
            id = uuid.uuid4()
            new_user = User.objects.create(id=id, full_name=user_data["full_name"], user_name=user_data["user_name"], email=user_data["email"], password=user_data["password"])
            new_user.save()
            serializer = serializers.UserSerializer(new_user)
            return Response(serializer.data)

class LoginAPIView(generics.GenericAPIView):
    user_name_param = openapi.Parameter('user_name', in_=openapi.IN_QUERY,type=openapi.TYPE_STRING)
    password_param = openapi.Parameter('password', in_=openapi.IN_QUERY,type=openapi.TYPE_STRING)
    throttle_scope = "users_app"

    @swagger_auto_schema(manual_parameters=[user_name_param, password_param])
    def post(self, request, *args, **kwargs):

        user_name = request.query_params["user_name"]
        password = request.query_params["password"]
        try:
            user = User.objects.get(user_name=user_name)

            if user.password == password:
                serializer = serializers.UserSerializer(user)
                return Response(serializer.data)
            else:
                return HttpResponse('Password incorrect.', status=404)
        except ObjectDoesNotExist:
                return HttpResponse("User doesn't exist", status=404)

class CategoryAPIView(generics.GenericAPIView):
    serializer_class = serializers.CategorySerializer
    throttle_scope = "categories_app"
    def post(self, request, *args, **kwargs):
        category_data = request.data

        checkExistName = User.objects.get(name=category_data["name"])
        if checkExistName:
            return HttpResponse("This category has existed!", status=404)
        else:
            id = uuid.uuid4()
            new_category = Category.objects.create(id=id, name=category_data["name"])
            new_category.save()
            serializer = serializers.CategorySerializer(new_category)
            return Response(serializer.data)

class FoodAPIView(generics.GenericAPIView):
    serializer_class = serializers.FoodSerializer
    throttle_scope = "foods_app"
    def post(self, request, *args, **kwargs):
        food_data = request.data
        id = uuid.uuid4()
        category = Category.objects.get(id = food_data["category_id"])
        new_food = Food.objects.create(id=id, name = food_data["name"], calorie = food_data["calorie"], potion = food_data["potion"], level = food_data["level"], star_level = food_data["star_level"], prepare = food_data["prepare"], youtube_url = food_data["youtube_url"], category=category)
        new_food.save()
        serializer = serializers.FoodSerializer(new_food)
        return Response(serializer.data)

class ReviewAPIView(generics.GenericAPIView):
    serializer_class = serializers.ReviewSerializer
    throttle_scope = "reviews_app"
    def post(self, request, *args, **kwargs):
        review_data = request.data
        id = uuid.uuid4()
        food = Food.objects.get(id = review_data["food_id"])
        new_review = Review.objects.create(id=id, content=review_data["content"], food = food)
        new_review.save()
        serializer = serializers.ReviewSerializer(new_review)
        return Response(serializer.data)

class UserFavoriteFoodAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserFavoriteFoodSerializer
    throttle_scope = "favorites_food_app"
    def post(self, request, *args, **kwargs):
        data = request.data
        id = uuid.uuid4()
        food = Food.objects.get(id = data["food_id"])
        user = User.objects.get(id = data["user_id"])
        new_fav = UserFavoriteFood.objects.create(id=id, food = food, user=user)
        new_fav.save()
        serializer = serializers.UserFavoriteFoodSerializer(new_fav)
        return Response(serializer.data)

class IngredientAPIView(generics.GenericAPIView):
    serializer_class = serializers.IngredientSerializer
    throttle_scope = "ingredients_app"
    def post(self, request, *args, **kwargs):
        data = request.data
        id = uuid.uuid4()
        new_ingredient = Ingredient.objects.create(id=id, name = data["name"])
        new_ingredient.save()
        serializer = serializers.IngredientSerializer(new_ingredient)
        return Response(serializer.data)

class FoodIngredientAPIView(generics.GenericAPIView):
    serializer_class = serializers.FoodIngredientSerializer
    throttle_scope = "food_ingredient_app"
    def post(self, request, *args, **kwargs):
        data = request.data
        id = uuid.uuid4()
        food = Food.objects.get(id = data["food_id"])
        ingredient = Ingredient.objects.get(id = data["ingredient_id"])
        new_food_ingredient = FoodIngredient.objects.create(id=id, food = food, ingredient = ingredient, quantity = data["quantity"])
        new_food_ingredient.save()
        serializer = serializers.FoodIngredientSerializer(new_food_ingredient)
        return Response(serializer.data)
