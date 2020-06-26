from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.quickstart.views import (
    UserViewSet,
    GroupViewSet,
    AgencyViewSet
)

schema_view = get_schema_view(
    openapi.Info(
        title="DMS Nam Phat API",
        default_version='v1',
        description="DMS Nam Phat API docs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="trungpt.dev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'agencies', AgencyViewSet)

urlpatterns = [
    # Swagger endpoints
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    # Get token
    path('api-auth-token/', obtain_auth_token, name='api_token_auth'),
    #OTP
    path('', include('drfpasswordless.urls')),
    # API endpoints
    path('', include(router.urls))
]
