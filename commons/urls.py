from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth.views import LoginView

from rest_framework import routers
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import (
    CustomObtainAuthToken,  # Tokens
    LoginView,              # Sessions
    UserViewSet,
    ProfileViewSet,
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
    ProductUnitTypeViewSet,
    ProductViewSet,
    MasterProductPriceViewSet
)
from storages.views import StorageViewSet
from areas.views import (
    AreaViewSet,
    AreaSalesmanViewSet,
    AreaAgencyViewSet
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
router.register(r'permissions', PermissionViewSet)
router.register(r'profiles', ProfileViewSet)

router.register(r'agencies', AgencyViewSet)
router.register(r'request-orders', RequestOrderViewSet)
router.register(r'agreed-orders', AgreedOrderViewSet)

router.register(r'products', ProductViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'product-unit-types', ProductUnitTypeViewSet)
router.register(r'product-master-prices', MasterProductPriceViewSet)

router.register(r'areas', AreaViewSet)
router.register(r'area-salesman', AreaSalesmanViewSet)
router.register(r'area-agency', AreaAgencyViewSet)


router.register(r'storages', StorageViewSet)

urlpatterns = [
    # Swagger
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),

    # Auth
    path(r'auth/', CustomObtainAuthToken.as_view(), name='api_token'),
    path(r'login/', LoginView.as_view(), name='login'),

    # OTP || TODO Custom auth endpoint
    path('', include('drfpasswordless.urls')),
    path('', include(router.urls)),
]
