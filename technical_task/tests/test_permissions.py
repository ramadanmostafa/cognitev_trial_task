from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

from technical_task.permissions import IsAuthenticated


class TestIsAuthenticatedPermission(TestCase):
    def setUp(self):
        self.permission = IsAuthenticated()
        self.request = RequestFactory().post('/api/status/')

    def test_has_permission_with_none_parameters(self):
        self.assertFalse(self.permission.has_permission(None, None))

    def test_has_permission_with_empty_parameters(self):
        self.assertFalse(self.permission.has_permission("", ""))

    def test_with_empty_request(self):
        self.assertFalse(self.permission.has_permission(self.request, ""))

    def test_add_wrong_meta_to_request(self):
        self.request.user = User.objects.create(username="TestUser")
        self.request.META = {"HTTP_AUTHORIZATION": "123"}
        self.assertFalse(self.permission.has_permission(self.request, ""))

    def test_add_right_meta_to_request(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        self.request.user = User.objects.create(username="TestUser")

        payload = jwt_payload_handler(self.request.user)
        self.request.META = {"HTTP_AUTHORIZATION": "token {}".format(jwt_encode_handler(payload))}
        self.assertTrue(self.permission.has_permission(self.request, ""))
