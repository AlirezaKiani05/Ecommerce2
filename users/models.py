from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Country(models.Model):
    name = models.CharField(max_length=40)
    abbr = models.CharField(max_length=4)  # Abbreviation
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    phone_regex = RegexValidator(
        regex=r'^98\d{10}$', message="The phone number should begin with 98")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.ForeignKey(
        to=Country, on_delete=models.PROTECT, default=1)
    avatar = models.ImageField(blank=True, upload_to='profile_avatars/')

    def __str__(self):
        return f'{self.user}-{self.phone_number}'


# class Device(models.Model):
#     DEVICE_WEB = 1
#     DEVICE_IOS = 2
#     DEVICE_ANDROID = 3
#     DEVICE_PC = 4
#     DEVICE_CHOISES = (
#         (DEVICE_WEB, ('web device')),
#         (DEVICE_IOS, ('ios device')),
#         (DEVICE_ANDROID, ('andriod device')),
#         (DEVICE_PC, ('pc device')),
#     )
#     user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
#                              related_name='devices', on_delete=models.CASCADE)
#     device_uuid = models.UUIDField('device UUID', null=True)
#     last_login = models.DateTimeField('last login date', null=True)
#     device_type = models.IntegerField(choices=DEVICE_CHOISES, default=1)
#     device_os = models.CharField('device os', max_length=20, blank=True)
#     device_model = models.CharField('device model', max_length=25, blank=True)
#     app_verssion = models.CharField(max_length=28)
#     created_time = models.DateTimeField(auto_now_add=True)
