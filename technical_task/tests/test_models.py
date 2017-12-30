from django.test import TestCase
from django.contrib.auth.models import User

from technical_task.models import avatar_directory_path, Profile


class TestAvatarDirPath(TestCase):
    def test_with_empty_parameters(self):
        self.assertEqual("avatar/", avatar_directory_path("", ""))

    def test_with_none_parameters(self):
        self.assertEqual("avatar/None", avatar_directory_path(None, None))

    def test_with_actual_parameters(self):
        self.assertEqual("avatar/test.jpg", avatar_directory_path("", "test.jpg"))


class TestProfileSaveMethod(TestCase):
    def setUp(self):
        self.profile = Profile()
        self.profile.first_name = "Test"
        self.profile.last_name = "User"
        self.profile.country_code = "EG"
        self.profile.phone_number = "01116620840"
        self.profile.gender = "male"
        self.profile.birthdate = "1990-08-02"
        self.profile.password = "12345678"
        self.profile.save()

    def test_save_user_created(self):
        self.assertEqual(1, User.objects.filter(username="01116620840").count())
        self.assertEqual(1, Profile.objects.filter(phone_number="01116620840").count())

    def test_save_user_updated(self):
        self.profile.phone_number = "123"
        self.profile.save()
        self.profile.user.username = "123"
        self.profile.user.save()
        self.assertEqual(1, User.objects.filter(username="123").count())
        self.assertEqual(1, Profile.objects.filter(phone_number="123").count())