from django.urls import path
#from .views import UploadFileViewSet
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views

SchemaView = get_schema_view(
    openapi.Info(
        title="API for mobile final",
        default_version='v1',
        description="Document for API",
        terms_of_service="https://www.pbl5.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('users/sign-up', views.SignUpAPIView.as_view()),
    path('users/log-in', views.LoginAPIView.as_view()),
    path('categories', views.CategoryAPIView.as_view()),
    path('ingredients/', views.IngredientAPIView.as_view()),
    path('upload/image', views.UploadImageAPIView.as_view()),
    path('doc',
         SchemaView.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         SchemaView.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
