from rest_framework import serializers

from .models import *

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

class ServiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDetails
        fields = '__all__'

