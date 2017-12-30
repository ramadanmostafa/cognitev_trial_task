from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class TestUserCreateAPIView(APITestCase):
    def setUp(self):
        self.data = {
            "gender": "male",
            "last_name": "last name",
            "country_code": "EG",
            "birthdate": "1990-08-02",
            "phone_number": "01116620840",
            "first_name": "first name",
            "password": "12345678",
            "email": "ramadan@test.com",
        }

    def test_method_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(405, response.status_code)

    def test_method_post_invalid(self):
        del self.data["password"]
        response = self.client.post(reverse('register'), data=self.data)
        self.assertEqual(400, response.status_code)

    def test_method_post_valid(self):

        response = self.client.post(reverse('register'), data=self.data)
        self.assertEqual(201, response.status_code)


class TestUserLoginAPIView(APITestCase):

    def setUp(self):
        self.password = "123456789"
        self.phone_number = "01116620840"
        self.user = User.objects.create(username=self.phone_number)
        self.user.set_password(self.password)
        self.user.save()

    def test_method_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(405, response.status_code)

    def test_method_post_invalid(self):
        data = {
            "phone_number": self.phone_number,
            "password": self.password + "0"
        }
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(400, response.status_code)

    def test_method_post_valid(self):
        data = {
            "phone_number": self.phone_number,
            "password": self.password
        }
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(200, response.status_code)


class TestUserStatusCreateAPIView(APITestCase):
    def setUp(self):
        self.token = ""
        self.password = "123456789"
        self.phone_number = "01116620840"
        self.user = User.objects.create(username=self.phone_number)
        self.user.set_password(self.password)
        self.user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = "token {}".format(jwt_encode_handler(payload))

    def test_method_get_without_token(self):
        response = self.client.get(reverse('post_status'))
        self.assertEqual(401, response.status_code)

    def test_method_post_without_token(self):
        response = self.client.post(reverse('post_status'))
        self.assertEqual(401, response.status_code)

    def test_method_get_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(reverse('post_status'))
        self.assertEqual(405, response.status_code)

    def test_post_with_valid_data(self):
        data = {
            "status": "I AM OK"
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(reverse('post_status'), data=data)
        self.assertEqual(201, response.status_code)
