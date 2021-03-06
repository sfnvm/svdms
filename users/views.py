import logging

from django.shortcuts import render
from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.filters import SearchFilter

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action

from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend


from users.serializers import UserSerializer, ProfileSerializer
from users.models import (
    User as UserModel,
    Profile as ProfileModel
)
from agencies.models import (
    Agency as AgencyModel
)
from agencies.serializers import (
    AgencySerializer
)

from commons import mails_worker

logger = logging.getLogger(__name__)


@api_view
def get_current_profile(request):  # Need it?
    pass


class LoginView(APIView):  # Session login
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        username = request.data['username']
        password = request.data['password']

        logger.debug('Attempt authentication with %s : "%s"' %
                     (username, password,))
        # Attempt authentication
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # Care for the session
                login(request, user)
                # see the expiration to 0 if remember wasn't requested

                # if not remember:
                #     request.session.set_expiry(0)

                # Return successful response
                logger.debug('Login successfully')
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
        # serialized_obj = serializers.serialize('json', token.user)

        # addition infor for agency login
        user_instance = token.user
        agency_instance = AgencyModel.objects.filter(
            user_related=user_instance).values()

        # mails_worker.test('trungpt.dev@gmail.com', user_instance.username)

        if(agency_instance):
            return Response({
                'token': token.key,
                'id': token.user_id,
                'first_name': token.user.first_name,
                'last_name': token.user.last_name,
                'email': token.user.email,
                'role': token.user.role,
                'agency': list(agency_instance)
            })
        return Response({
            'token': token.key,
            'id': token.user_id,
            'first_name': token.user.first_name,
            'last_name': token.user.last_name,
            'email': token.user.email,
            'role': token.user.role
        })


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all().order_by(
        '-date_joined')
    serializer_class = UserSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, )
    filterset_fields = {
        'username': ['contains'],
        'role': ['exact'],
        'is_active': ['exact']
    }
    search_fields = ['username', 'email']

    # Custom action to lockuser by id
    @action(detail=True, methods=['put'])
    def lock_user(self, request, pk=None):
        queryset = UserModel.objects.filter(pk=pk)
        queryset.update(is_active=False)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data[0])

    # Custom action to reactivate user by id
    @action(detail=True, methods=['put'])
    def reactivate(self, request, pk=None):
        queryset = UserModel.objects.filter(pk=pk)
        queryset.update(is_active=True)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data[0])


class ProfileViewSet(ModelViewSet):
    queryset = ProfileModel.objects.all().order_by('id')
    serializer_class = ProfileSerializer
