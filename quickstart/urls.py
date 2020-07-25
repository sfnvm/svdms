from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import LoginView

from rest_framework import routers
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authentication import SessionAuthentication, BaseAuthentication

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from quickstart import views as app_views

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

router.register(r'users', app_views.UserViewSet)
router.register(r'groups', app_views.GroupViewSet)
router.register(r'permissions', app_views.PermissionViewSet)
router.register(r'profiles', app_views.ProfileViewSet)

router.register(r'agencies', app_views.AgencyViewSet)
router.register(r'request-orders', app_views.RequestOrderViewSet)
router.register(r'agreed-orders', app_views.AgreedOrderViewSet)

router.register(r'products', app_views.ProductViewSet)
router.register(r'product-types', app_views.ProductTypeViewSet)
router.register(r'product-unit-types', app_views.ProductUnitPyteViewSet)

router.register(r'storages', app_views.StorageViewSet)

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
    path(r'auth/', app_views.CustomObtainAuthToken.as_view(), name='api_token'),
    # Session token
    path(r'login/', LoginView.as_view(), name='login'),
    # OTP
    path('', include('drfpasswordless.urls')),
    # API endpoints with Router
    path('', include(router.urls)),
    # Check authen
    path('auth/check/', app_views.check_token, name='check_token'),
    # Grant permission
    #
    # Optional User endpoints (use APIView to override)
    # url(r'users/', UserViewSet.as_view(), name='user'),
    # Optional Group endpoints (use APIView to override)
    #
    # Optional Agency endpoints (use APIView to override)
    #
    # Optional Product endpoints (use APIView to override)
    #
    # Optional Storage endpoints (use APIView to override)
    #
    # Optional Order endpoints (use APIView to override)
]
