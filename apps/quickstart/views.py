from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import response

from apps.quickstart.models import (
    Agency
)

from apps.quickstart.serializers import (
    UserSerializer,
    GroupSerializer,
    AgencySerializer
)


#####################
##### User Auth #####
#####################

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


###############
##### OTP #####
###############


###########################
##### Other Endpoints #####
###########################

class AgencyViewSet(ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
