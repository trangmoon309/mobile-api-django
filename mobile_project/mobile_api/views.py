from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http.response import FileResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.parsers import (FileUploadParser, FormParser,
                                    MultiPartParser)
from rest_framework.response import Response

from mobile_api.forms import ImageForm

from . import serializers
from .models import Category, Food, FoodIngredient, Image, Ingredient, User


class SignUpAPIView(generics.GenericAPIView):
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


class ImageAPIView(generics.GenericAPIView):
    serializer_class = serializers.ImageSerializer
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image = form.instance
            serializer = serializers.ImageSerializer(image)
            return Response(serializer.data)
        return Response(status=400)

    id_param = openapi.Parameter('id',
                                    in_=openapi.IN_QUERY,
                                    type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[id_param])
    def get(self, request):
        image_instance = Image.objects.get(id=request.query_params['id'])
        img = open(image_instance.image.url, 'rb')
        return HttpResponse(img, content_type="image/jpeg")


class FoodAPIView(generics.GenericAPIView):
    @swagger_auto_schema(request_body=serializers.FoodSerializer)
    def post(self, request):
        food_data = request.data

        category = Category.objects.get(id=food_data['category_id'])
        cover_image = Image.objects.get(id=food_data['cover_image_id'])

        new_food = Food.objects.create(
            name=food_data['name'],
            clorie='clorie' in food_data and food_data['clorie'] or None,
            potion='potion' in food_data and food_data['potion'] or None,
            level='level' in food_data and food_data["level"] or None,
            star_level='start_level' in food_data and food_data["star_level"]
            or None,
            prepare=food_data["prepare"],
            youtube_url='youtube_url' in food_data and food_data["youtube_url"]
            or None,
            cover_image=cover_image,
            category=category)

        detail_ingredients = food_data['detail_ingredients']
        for detail_ingredient in detail_ingredients:
            ingredient = Ingredient.objects.get(
                id=detail_ingredient['ingredient_id'])

            FoodIngredient.objects.create(
                food=new_food,
                ingredient=ingredient,
                quantity=detail_ingredient['quantity'])

        return Response("Create sucessfully")
