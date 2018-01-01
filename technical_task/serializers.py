from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Profile, UserStatus


class UserCreateSerializer(serializers.ModelSerializer):
    """
    serializer for create user view
    """
    password = serializers.CharField(min_length=8, max_length=256, required=True)

    def validate(self, data):
        """
        additional validation for the phone number, should be at least 11 digits without the + sign
        :param data:
        :return:
        """
        if "phone_number" in data:
            user_query = User.objects.filter(username=data["phone_number"])
            if user_query.exists():
                raise ValidationError(
                    {'phone_number': "This phone number is already registered. Please login instead."}
                )
            if len(data["phone_number"]) == 11 and data["phone_number"].isdigit():
                return data
            if len(data["phone_number"]) > 11 and data["phone_number"].startswith("+") and data["phone_number"][1:].isdigit():
                return data
        raise ValidationError(
            {'phone_number': "Invalid phone number. It should be at least 11 digits."}
        )

    class Meta:
        model = Profile
        fields = (
            'id',
            'first_name',
            'last_name',
            'country_code',
            'phone_number',
            'gender',
            'birthdate',
            'avatar',
            'email',
            'password',
        )


class UserLoginSerializer(serializers.ModelSerializer):
    """
    serializer for user login view
    """

    def validate(self, data):
        """
        make sure the phone number is already registered
        :param data:
        :return:
        """
        user = authenticate(username=data["phone_number"], password=data["password"])
        if user is None:
            raise ValidationError(
                "Invalid phone number or password"
            )
        
        return data

    class Meta:
        model = Profile
        fields = (
            'phone_number',
            'password',
        )


class UserStatusSerializer(serializers.ModelSerializer):
    """
    serializer for create user status view
    """
    class Meta:
        model = UserStatus
        fields = (
            "id",
            "status",
        )
