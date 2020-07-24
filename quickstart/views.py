from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication, BasicAuthentication

# Somewhat easy to use
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.permissions import DjangoModelPermissions

from quickstart import models as app_models
from quickstart import serializers as app_serializers


@api_view  # simple endpoint to check credential
def check_token(request):
    """
    Check token
    """
    if request.method == 'POST':
        content = {'details': 'Token is OK!'}
        return Response(content)


@api_view  # Get peronal information
def get_current_profile(request):
    pass


# class ExampleAuthentication(authentication.BaseAuthentication):

#     def authenticate(self, request):

#         # Get the username and password
#         username = request.data.get('username', None)
#         password = request.data.get('password', None)

#         if not username or not password:
#             raise exceptions.AuthenticationFailed(
#                 _('No credentials provided.'))

#         credentials = {
#             get_user_model().USERNAME_FIELD: username,
#             'password': password
#         }

#         user = authenticate(**credentials)

#         if user is None:
#             raise exceptions.AuthenticationFailed(
#                 _('Invalid username/password.'))

#         if not user.is_active:
#             raise exceptions.AuthenticationFailed(
#                 _('User inactive or deleted.'))

#     return (user, None)  # authentication successful

# class MyBasicAuthentication(BasicAuthentication):

#     def authenticate(self, request):
#         user, _ = super(MyBasicAuthentication, self).authenticate(request)
#         login(request, user)
#         return user, _


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined').filter(is_active=True)
    serializer_class = app_serializers.UserSerializer
    # permission_classes = [permissions.IsAdminUser, ]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = app_serializers.GroupSerializer
    # permission_classes = [permissions.IsAdminUser, ]


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = app_serializers.PermissionSerializer


class ProfileViewSet(ModelViewSet):
    queryset = app_models.Profile.objects.all().order_by('id')
    serializer_class = app_serializers.ProfileSerializer


class AgencyViewSet(ModelViewSet):
    queryset = app_models.Agency.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.AgencySerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance = self.get_object()
        if(instance.removed == False):
            instance.removed_by = self.request.user
            instance.removed = True
            instance.save()
        else:
            return Response({'details': 'Not found'}, status=404)


class ProductViewSet(ModelViewSet):
    queryset = app_models.Product.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.ProductSerializer


class ProductTypeViewSet(ModelViewSet):
    queryset = app_models.ProductType.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.ProductTypeSerializer


class MasterProductPriceViewSet(ModelViewSet):
    queryset = app_models.MasterProductPrice.objects.all().order_by(
        'id').filter(removed=False)
    serializer_class = app_serializers.MasterProductPriceSerializer


class RequestOrderViewSet(ModelViewSet):
    queryset = app_models.RequestOrder.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.RequestOrderSerializer


class AgreedOrderViewSet(ModelViewSet):
    queryset = app_models.AgreedOrder.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.AgreedOrderSerializer


class StorageViewSet(ModelViewSet):
    queryset = app_models.Storage.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.StorageSerializer
