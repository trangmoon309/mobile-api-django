from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.decorators import parser_classes


from .models import User, Food, UserFavoriteFood, Ingredient, FoodIngredient, Review, Category
from .serializers import UserFavoriteFood, LoginSerializer, UserSerializer
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render

class UserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    throttle_scope = "users_app"

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class SignUpAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
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
            serializer = UserSerializer(new_user)
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
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return HttpResponse('Password incorrect.', status=404)
        except ObjectDoesNotExist:
                return HttpResponse("User doesn't exist", status=404)