from rest_framework.permissions import BasePermission
from rest_framework_jwt.utils import jwt_decode_handler

from django.contrib.auth.models import User


class IsAuthenticated(BasePermission):

    message = 'Invalid auth token.'

    def has_permission(self, request, view):

        try:
            header_token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return False
        if header_token:
            try:
                token = header_token.split(' ')[1]
                payload = jwt_decode_handler(token)
                obj = User.objects.get(id=payload['user_id'])
            except:
                return False
            else:
                return obj == request.user