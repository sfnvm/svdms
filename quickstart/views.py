from django.shortcuts import render
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model, authenticate, login

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework import filters

from rest_framework.decorators import api_view
from rest_framework.response import Response

from quickstart import models as app_models
from quickstart import serializers as app_serializers

User = get_user_model()


@api_view(['GET'])  # simple endpoint to check credential
def check_token(request):
    """
    Check token
    """
    content = {'details': 'Token is OK!'}
    return Response(content)


@api_view  # Get peronal information
def get_current_profile(request):
    pass


class LoginView(APIView):  # Session login
    serializer_class = app_serializers.UserSerializer

    def post(self, request, *args, **kwargs):

        username = request.data['username']
        password = request.data['password']
        remember = request.data['remember']

        # logger.debug('Attempt authentication with %s : "%s"' %
        #              (username, password,))
        # Attempt authentication
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # Care for the session
                login(request, user)
                # se the expiration to 0 if remember wasn't requested
                if not remember:
                    request.session.set_expiry(0)
                # Return successful response
                # logger.debug('Login successfully')
                return Response(self.serializer_class(user).data)
            else:
                logger.warn('User %s is de-activated' % username)
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            logger.debug('Unauthorized access with %s : "%s"' %
                        (username, password,))
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs
        )
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined').filter(is_active=True)
    serializer_class = app_serializers.UserSerializer
    # permission_classes = [permissions.IsAdminUser, ]

    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


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


class ProductTypeViewSet(ModelViewSet):
    queryset = app_models.ProductType.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.ProductTypeSerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance = self.get_object()
        if(instance.removed == False):
            instance.removed_by = self.request.user
            instance.removed = True
            instance.save()


class ProductUnitPyteViewSet(ModelViewSet):
    queryset = app_models.ProductUnitType.objects.all().order_by(
        'id').filter(removed=False)
    serializer_class = app_serializers.ProductUnitTypeSerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance = self.get_object()
        if(instance.removed == False):
            instance.removed_by = self.request.user
            instance.removed = True
            instance.save()


class ProductViewSet(ModelViewSet):
    queryset = app_models.Product.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.ProductSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance = self.get_object()
        if(instance.removed == False):
            instance.removed_by = self.request.user
            instance.removed = True
            instance.save()


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
