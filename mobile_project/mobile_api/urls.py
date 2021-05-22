from django.urls import path, include
from . import views
#from .views import UploadFileViewSet
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
   openapi.Info(
      title="API for mobile final",
      default_version='v1',
      description="Document for API",
      terms_of_service="https://www.pbl5.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('users', views.UserAPIView.as_view()),   
   path('users/sign-up', views.SignUpAPIView.as_view()),   
   path('users/log-in', views.LoginAPIView.as_view()),
   path('categories', views.CategoryAPIView.as_view()),
   path('foods/', views.FoodAPIView.as_view()), 
   path('foods/by-ingredient', views.FoodByIngredientAPIView.as_view()),     
   path('reviews/', views.ReviewAPIView.as_view()),
   path('ingredients/', views.IngredientAPIView.as_view()),
   #path('food-ingredients/', views.FoodIngredientAPIView.as_view()),
   path('user-fav-foods/', views.UserFavoriteFoodAPIView.as_view()),
   path('doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]