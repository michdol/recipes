from django.contrib.postgres.fields import JSONField
from django.db import models

from recipes.constants import RECIPE_STATUS_CREATED, RECIPE_STATUS_CHOICES


class SourceWebsite(models.Model):
	name = models.CharField(max_length=128, verbose_name="name")
	url = models.CharField(max_length=1024, verbose_name="url")
	is_active = models.BooleanField(default=True, verbose_name="is active")

	class Meta:
		verbose_name = "source website"
		verbose_name_plural = "source websites"


class Recipe(models.Model):
	source = models.ForeignKey(SourceWebsite, on_delete=models.DO_NOTHING, related_name="recipes",
							   verbose_name="source website")
	name = models.CharField(max_length=256, verbose_name="name")
	url = models.CharField(max_length=1024, unique=True, verbose_name="url")
	ingredients = models.TextField(verbose_name="ingredients")
	directions = models.TextField(verbose_name="directions")
	ingredients_json = JSONField(default=list, verbose_name="ingredients json")
	directions_json = JSONField(default=list, verbose_name="directions json")
	image_url = models.CharField(max_length=1024, blank=True, verbose_name="image url")
	status = models.SmallIntegerField(default=RECIPE_STATUS_CREATED, choices=RECIPE_STATUS_CHOICES,
									  verbose_name="status")
	extra = JSONField(default=dict, verbose_name="extra data")
	created = models.DateTimeField(auto_now_add=True, verbose_name="created")
	updated = models.DateTimeField(auto_now=True, verbose_name="updated")

	class Meta:
		verbose_name = "recipe"
		verbose_name_plural = "recipes"
