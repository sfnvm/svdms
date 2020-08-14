from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth.views import LoginView

from rest_framework import routers
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from quickstart import views as app_views
from users.views import (
    CustomObtainAuthToken,  # Tokens
    LoginView,              # Sessions
    UserViewSet,
    ProfileViewSet,
    check_token,
)
from permissions.views import (
    GroupViewSet,
    PermissionViewSet
)
from agencies.views import AgencyViewSet
from orders.views import (
    RequestOrderViewSet,
    AgreedOrderViewSet
)
from products.views import (
    ProductTypeViewSet,
    ProductUnitPyteViewSet,
    ProductViewSet
)
from storages.views import StorageViewSet

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
router.register(r'permissions', PermissionViewSet)
router.register(r'profiles', ProfileViewSet)

router.register(r'agencies', AgencyViewSet)
router.register(r'request-orders', RequestOrderViewSet)
router.register(r'agreed-orders', AgreedOrderViewSet)

router.register(r'products', ProductViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'product-unit-types', ProductUnitPyteViewSet)

router.register(r'storages', StorageViewSet)

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
    path(r'auth/', CustomObtainAuthToken.as_view(), name='api_token'),
    # Session token
    # path(r'login/', LoginView.as_view(), name='login'),
    path(r'login/', LoginView.as_view(), name='login'),
    # OTP
    path('', include('drfpasswordless.urls')),
    # API endpoints with Router
    path('', include(router.urls)),
    # Check authen
    path('auth/check/', check_token, name='check_token'),
    # Lock user
    re_path(r'users/^(?P<pk>[0-9]+)/$', UserViewSet.lock_user),
    # Confim RQO
    re_path(r'request-orders/^(?P<pk>[0-9]+)/$', RequestOrderViewSet.confirm)
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
