from rest_framework import serializers
from .models import UserPhotoInfo


class UserPhotoInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = UserPhotoInfo
        fields = '__all__'