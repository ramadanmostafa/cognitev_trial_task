from django.test import TestCase
from technical_task.serializers import UserCreateSerializer, UserLoginSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class TestUserCreateSerializer(TestCase):

    def setUp(self):
        self.serializer = UserCreateSerializer()

    def test_validate_empty_phone_number(self):
        with self.assertRaises(ValidationError) as context:
            self.serializer.validate({"phone_number": ""})

        self.assertIn('Invalid phone number. It should be at least 11 digits.', str(context.exception))

    def test_validate_used_phone_number(self):
        User.objects.create(username="01116620840")
        with self.assertRaises(ValidationError) as context:
            self.serializer.validate({"phone_number": "01116620840"})

        self.assertIn('This phone number is already registered. Please login instead.', str(context.exception))

    def test_valid_phone_number(self):
        data = {"phone_number": "01116620840"}
        self.assertEqual(data, self.serializer.validate(data))

    def test_valid_phone_number2(self):
        data = {"phone_number": "+201116620840"}
        self.assertEqual(data, self.serializer.validate(data))


class TestUserLoginSerializer(TestCase):

    def setUp(self):
        self.serializer = UserLoginSerializer()
        self.password = "123456789"
        self.phone_number = "01116620840"
        self.user = User.objects.create(username=self.phone_number)
        self.user.set_password(self.password)
        self.user.save()

    def test_with_invalid_data(self):
        data = {
            "phone_number": self.phone_number,
            "password": self.password + "1"
        }
        with self.assertRaises(ValidationError) as context:
            self.serializer.validate(data)

        self.assertIn('Invalid phone number or password', str(context.exception))

    def test_with_valid_data(self):
        data = {
            "phone_number": self.phone_number,
            "password": self.password
        }
        self.assertEqual(data, self.serializer.validate(data))
