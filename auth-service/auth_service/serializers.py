from rest_framework import serializers

from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = UserProfile
        depth = 0
        fields = ('id', 'instagram_username')


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    password = serializers.CharField(write_only=True)
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
            'user_profile', 'password')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        if user is not None:
            password = validated_data.get('password', None)
            if password is not None:
                print('password is not none')
                user.set_password(password)
            else:
                print('pw id none')
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        # retrieve the UserProfile
        profile_data = validated_data.pop('profile', None)
        for attr, value in profile_data.items():
            setattr(instance.profile, attr, value)

        # retrieve the User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        new_password = validated_data.get('password', None)
        if new_password is not None:
            instance.set_password(new_password)

        instance.profile.save()
        instance.save()
        return instance
