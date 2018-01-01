from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserCreateSerializer, UserLoginSerializer, UserStatusSerializer
from .permissions import IsAuthenticated
from .models import UserStatus


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserCreateAPIView(CreateAPIView):
    """
    create a new user view
    """
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class UserLoginAPIView(APIView):
    """
    login user view, if the user is already register, it will returns a unique token to be used further
    """
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():

            associated_user = User.objects.get(username=serializer.data['phone_number'])
            payload = jwt_payload_handler(associated_user)

            return Response(
                data={
                    'token': jwt_encode_handler(payload)
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserStatusCreateAPIView(CreateAPIView):
    """
    for authenticated users only, create status linked to this user,
    require HTTP_AUTHORIZATION: token {access_token}
    """

    serializer_class = UserStatusSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        if serializer.is_valid():
            UserStatus.objects.create(
                user=self.request.user,
                status=serializer.validated_data["status"]
            )