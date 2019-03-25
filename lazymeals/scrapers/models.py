from django.db import models


class Scraper(models.Model):
	name = models.CharField(max_length=128, unique=True, verbose_name='name')
	source = models.ForeignKey('recipes.SourceWebsite', on_delete=models.CASCADE, related_name='+',
							   verbose_name='source')

	class Meta:
		verbose_name = 'scraper'
		verbose_name_plural = 'scrapers'


class ScraperLog(models.Model):
	scraper = models.ForeignKey(Scraper, on_delete=models.CASCADE, related_name='logs', verbose_name='scraper')
	is_success = models.BooleanField(default=True, verbose_name='is success')
	started = models.DateTimeField(auto_now_add=True, verbose_name='started')
	finished = models.DateTimeField(null=True, blank=True, verbose_name='finished')

	class Meta:
		verbose_name = 'scraper log'
		verbose_name_plural = 'scraper logs'
