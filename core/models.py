from string import lower, capitalize
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    job_title = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'

    def get_screen_name(self):
        if self.user.first_name and self.user.last_name:
            return "{} {}".format(capitalize(lower(self.user.first_name)), capitalize(lower(self.user.last_name)))
        else:
            return self.user.username


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
