from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	image_url = models.CharField(max_length=256, blank=True, verbose_name="image url")

	class Meta:
		verbose_name = "user"
		verbose_name_plural = "users"
