from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import FileResponse

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from mobile_api.forms import ImageForm
from .models import User, Ingredient, Category
from . import serializers


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


class UploadImageAPIView(generics.GenericAPIView):
    serializer_class = serializers.ImageSerializer
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image = form.instance
            print(image.image.url)
            return FileResponse()
        return Response()
