import json
import logging
import operator
import requests

from bs4 import BeautifulSoup
from time import sleep

from django.conf import settings
from django.db import connection

from recipes.constants import RECIPE_STATUS_CREATED
from recipes.models import SourceWebsite
from scrapers.constants import SCRAPER_NAME_TASTY, SCRAPER_NAME_TASTY_API
from scrapers.models import Scraper, ScraperLog

logger = logging.getLogger(getattr(settings, 'LOG_ROOT'))

DELAYS = [1, 1.5, 2, 2.5, 3, 3.5]


class BaseScrapper(object):
	DEFAULT_PAGE_SIZE = 20
	USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
	REFERER = "https://www.google.jp"
	BASE_URL = None
	SCRAPER_NAME = None

	def __init__(self, page_size=None):
		self.scraper = Scraper.objects.get(name=self.SCRAPER_NAME)
		self.source_id = self.scraper.source_id
		self.source = SourceWebsite.objects.get(id=self.scraper.source_id)
		assert self.BASE_URL is not None, 'BASE_URL must not be None'
		self.page_size = page_size if page_size else self.DEFAULT_PAGE_SIZE
		self.session = None
		self.scraper = None

	@property
	def can_run(self):
		return not ScraperLog.objects.filter(
			scraper_id=self.scraper.id,
			finished__isnull=True
		).exists()

	def main(self):
		try:
			self.prepare_session()
			self.scrape()
		except Exception as e:
			logger.error("Exception occurred: {}".format(e))
			return False
		logger.info(
			"Successfully finished scraping {}.".format(self.source.url))
		return True

	def prepare_session(self):
		self.session = requests.Session()

	def scrape(self):
		pass


import pdb
class TastyScrapper(BaseScrapper):
	BASE_URL = 'https://tasty.co/{}'
	SCRAPER_NAME = SCRAPER_NAME_TASTY
	def scrape(self):
	#recipes = Recipe.objects.filter(source_id=self.source.id, status=RECIPE_STATUS_CREATED)
		response = requests.get('https://tasty.co/recipe/dairy-free-chicken-fettuccine-alfredo')
		soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
		ingredients = soup.find('div', class_='ingredients__section')
		pdb.set_trace()
		#print(ingredients.encode('utf-8', 'ignore'))



class TastyApiScrapper(BaseScrapper):
	BASE_URL = 'https://tasty.co/{}'
	SCRAPER_NAME = SCRAPER_NAME_TASTY_API

	def __init__(self, page_size=None):
		super().__init__(page_size)
		self.api_base_url = self.BASE_URL.format('api/{}')
		self.recent_recipes_endpoint = "recipes/recent"
		self.api_url = self.api_base_url.format(self.recent_recipes_endpoint)
		self.api_params_template = "size={size}&from={from}&page={page}&from_offset={from_offset}&__amp_sour"
		self.page_size = page_size if page_size else self.DEFAULT_PAGE_SIZE
		self.session = None
		self.recipe_count = None
		self.requests_count = 0

	def get_next_page_params(self, previous=False, **kwargs):
		operator_ = operator.sub if previous else operator.add
		size = kwargs.get('size')
		from_ = kwargs.get('from')
		page = kwargs.get('page')
		if previous and from_ - size < 0 or page - 1 < 0:
			raise ValueError(
				"Invalid parameters: page - %s; from - %s" % (page, from_))
		kwargs['from'] = operator_(from_, size)
		kwargs['page'] = operator_(page, 1)
		return kwargs

	def scrape(self):
		params = {
			'size': self.page_size,
			'from': 0,
			'page': 1,
			'from_offset': 1
		}
		url = self.build_url(**params)
		while self.requests_count < 10:
			response = self.session.get(url)
			self.requests_count += 1
			response = response.json()
			items = response.get('items')
			if len(items) <= 0:
				break
			self.parse_response(response)
			self.create_recipes(response.get('items'))
			params = self.get_next_page_params(**params)
			url = self.build_url(**params)
			if not settings.TESTING:
				sleep(1)

	def build_url(self, **params):
		return "?".join([
			self.api_url,
			self.api_params_template.format(**params)
		])

	def parse_response(self, response):
		if response.get('status') != 'ok':
			raise ValueError('Response status \'%s\'' % response.get('status'))
		self.recipe_count = response.get('recipe_count')

	def create_recipes(self, items):
		values = self.generate_sql_values(items)
		with connection.cursor() as cursor:
			cursor.execute("""
				INSERT INTO recipes_recipe (source_id, name, url, image_url, extra, ingredients, directions, ingredients_json, directions_json, status, created, updated)
				VALUES {values}
				ON CONFLICT DO NOTHING;
			""".format(values=values))

	def generate_sql_values(self, items):
		values = []
		for item in items:
			values.append("({source_id},'{name}','{url}','{image_url}','{extra}','','','[]','[]',{status},current_timestamp,current_timestamp)".format(
				source_id=self.source_id,
				name=item.get('name'),
				url=self._create_tasty_url(item.get('slug'), item.get('type')),
				image_url=item.get('thumb_big'),
				extra=self.generate_json_value(item),
				status=RECIPE_STATUS_CREATED
			))
		return ','.join(values)

	def _create_tasty_url(self, slug, type_):
		return self.BASE_URL.format('{type}/{slug}/'.format(type=type_, slug=slug))

	def generate_json_value(self, item):
		return json.dumps({
			'id': item.get('id'),
            'tags': ','.join(item.get('tags')),
            'type': item.get('type'),
            'object_name': item.get('object_name')
        })
