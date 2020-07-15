from django.contrib.auth.models import (
    User,
    Group
)
from rest_framework import serializers

from apps.quickstart.models import (
    Profile,
    Agency,
    ProductType,
    ProductUnitType,
    Product,
    ProductType,
    MasterProductPrice,
    Order,
    Storage
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'
        # read_only_fields = ('created_at', 'updated_at')
        depth = 1
        # exclude = ['password']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.filter(user=user).update(**profile_data)
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class AgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class MasterProductPriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MasterProductPrice
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class StorageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
