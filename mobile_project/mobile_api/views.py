import uuid

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User, Food, UserFavoriteFood, Ingredient, FoodIngredient, Review, Category
from . import serializers


class UserAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    throttle_scope = "users_app"

    def get(self, request):
        users = User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    id_param = openapi.Parameter('id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[id_param])
    def delete(self, request, *args, **kwargs):
        User.objects.filter(id=request.query_params["id"]).delete()
        return Response("Success!")

    id_param = openapi.Parameter('id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[id_param])
    def put(self, request, *args, **kwargs):
        user_data = request.data
        updated_user = User.objects.get(id=request.query_params["id"])
        updated_user.full_name = user_data["full_name"]
        updated_user.user_name = user_data["user_name"]
        updated_user.email = user_data["email"]
        updated_user.password = user_data["password"]
        updated_user.save()
        serializer = serializers.UserSerializer(updated_user)
        return Response(serializer.data)


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    throttle_scope = "users_app"

    def post(self, request, *args, **kwargs):
        user_data = request.data

        try:
            User.objects.get(email=user_data["email"])
            return HttpResponse("Username has existed!", status=404)
        except ObjectDoesNotExist:
            new_user = User.objects.create(full_name=user_data["full_name"],
                                           email=user_data["email"],
                                           password=user_data["password"])
            new_user.save()
            serializer = serializers.UserSerializer(new_user)
            return Response(serializer.data)


class LoginAPIView(generics.GenericAPIView):
    email_param = openapi.Parameter('email',
                                    in_=openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING)
    password_param = openapi.Parameter('password',
                                       in_=openapi.IN_QUERY,
                                       type=openapi.TYPE_STRING)
    #  throttle_scope = "users_app"

    @swagger_auto_schema(manual_parameters=[email_param, password_param])
    def post(self, request, *args, **kwargs):

        email = request.query_params["email"]
        password = request.query_params["password"]
        try:
            user = User.objects.get(email=email)

            if user.password == password:
                serializer = serializers.UserSerializer(user)
                return Response(serializer.data)
            return HttpResponse('Password incorrect.', status=404)
        except ObjectDoesNotExist:
            return HttpResponse("User doesn't exist", status=404)


class CategoryAPIView(generics.GenericAPIView):
    serializer_class = serializers.CategorySerializer
    throttle_scope = "categories_app"

    @swagger_auto_schema(operation_description='Get all categories')
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)


class IngredientAPIView(generics.GenericAPIView):
    @swagger_auto_schema(operation_description='Get all ingredients')
    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = serializers.IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
