import logging
from rest_framework import serializers

from users.models import (
    User as UserModel,
    Profile as ProfileModel
)

logger = logging.getLogger(__name__)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        exclude = ['user']
        # duplicate error when update unique field with the same data
        extra_kwargs = {
            'code': {'validators': []},
        }


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = '__all__'
        read_only_fields = ('date_joined', 'is_superuser',
                            'is_staff', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        depth = 1

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        user = UserModel.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        ProfileModel.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()

        profile_instance = ProfileModel.objects.filter(user=user)

        if(profile_instance):
            profile_instance.update(**profile_data)
        else:
            ProfileModel.objects.create(user=user, **profile_data)

        return user

    def lock_user(self, instance, validated_data):
        pass
