from django.db import models
from django.contrib.auth.models import User

from . import COUNTRY_CODES, GENDERS


def avatar_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/<filename>
    return 'avatar/%s' % (filename, )


class Profile(models.Model):

    def save(self, *args, **kwargs):
        if not self.id:
            self.user = User.objects.get_or_create(username=self.phone_number)[0]
            self.user.set_password(self.password)
            self.user.save()
        super(Profile, self).save(*args, **kwargs)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    country_code = models.CharField(choices=COUNTRY_CODES, max_length=2)
    phone_number = models.CharField(max_length=13)
    gender = models.CharField(choices=GENDERS, max_length=6)
    birthdate = models.DateField()
    avatar = models.ImageField(upload_to=avatar_directory_path, null=True)
    email = models.EmailField(null=True, blank=True, max_length=256)
    password = models.CharField(max_length=256)


class UserStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.TextField()
