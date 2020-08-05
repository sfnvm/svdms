from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from agencies.serializers import AgencySerializer
from agencies.models import Agency as AgencyModel


class AgencyViewSet(ModelViewSet):
    queryset = AgencyModel.objects.all().order_by('id').filter(removed=False)
    serializer_class = AgencySerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    """
    Mark as removed
    """
    # def perform_destroy(self, request):
    #     instance = self.get_object()
    #     if(instance.removed == False):
    #         instance.removed_by = self.request.user
    #         instance.removed = True
    #         instance.save()

    def perform_destroy(self, request):
        instance.delete()
