from rest_framework import serializers
from agencies.models import Agency as AgencyModel


class AgencySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = AgencyModel
        fields = '__all__'
