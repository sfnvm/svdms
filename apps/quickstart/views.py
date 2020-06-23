from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import views
from rest_framework import viewsets
from rest_framework import response

from apps.quickstart.serializers import UserSerializer, GroupSerializer


class Ping(views.APIView):
    def get(self, request, format=None):
        return response.Response('pong!')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer