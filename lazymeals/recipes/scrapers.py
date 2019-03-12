import operator
from time import sleep

import requests

from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from recipes.constants import TASTY_SOURCE_ID
from recipes.models import SourceWebsite, Recipe


class TastyScrapper(object):
	DEFAULT_PAGE_SIZE = 20
	def __init__(self, page_size=None):
		self.website_id = TASTY_SOURCE_ID
		self.website = SourceWebsite.objects.get(id=self.website_id)
		self.base_url = 'https://tasty.co/{}'
		self.api_base_url = self.base_url.format('api/{}')
		self.recent_recipes_endpoint = "recipes/recent"
		self.api_url = self.api_base_url.format(self.recent_recipes_endpoint)
		self.api_params_template = "size={size}&from={from}&page={page}&from_offset={from_offset}&__amp_sour"
		self.page_size = page_size if page_size else self.DEFAULT_PAGE_SIZE
		self.session = None
		self.recipe_count = None
		self.requests_count = 0

		"https://tasty.co/api/recipes/recent?size=20&from=20&page=2&from_offset=1&__amp_s"
		"https://tasty.co/api/recipes/recent?size=20&from=40&page=3&from_offset=1&__amp_sour"
		"https://tasty.co/api/recipes/recent?size=20&from=60&page=4&from_offset=1&__amp_sour"

	def build_url(self, **params):
		return "?".join([
			self.api_url,
			self.api_params_template.format(**params)
		])

	@property
	def initial_params(self):
		return {
			'size': self.page_size,
			'from': 0,
			'page': 1,
			'from_offset': 1
		}

	def get_next_page_params(self, previous=False, **kwargs):
		operator_ = operator.sub if previous else operator.add
		size = kwargs.get('size')
		from_ = kwargs.get('from')
		page = kwargs.get('page')
		if previous and from_ - size < 0 or page -1 < 0:
			raise ValueError("Invalid parameters: page - %s; from - %s" % (page, from_))
		kwargs['from'] = operator_(from_, size)
		kwargs['page'] = operator_(page, 1)
		return kwargs

	def main(self):
		try:
			self.session = requests.Session()
			self.scrape()
		except Exception as e:
			print("Exception occurred", e)
			return False
		print("Process finished successfully.")
		return True

	def scrape(self):
		params = self.initial_params
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
			sleep(1)

	def parse_response(self, response):
		if response.get('status') != 'ok':
			raise ValueError('Response status \'%s\'' % response.get('status'))
		self.recipe_count = response.get('recipe_count')

	def create_recipes(self, items):
		recipes = []
		for item in items:
			recipes.append(Recipe(
				source_id=self.website_id,
				name=item.get('name'),
				url=self._create_tasty_url(item.get('slug'), item.get('type')),
				image_url=item.get('thumb_big'),
				extra={
					'id': item.get('id'),
					'tags': ','.join(item.get('tags')),
					'type': item.get('type'),
					'object_name': item.get('object_name')
				}
			))
		Recipe.objects.bulk_create(recipes)

	def _create_tasty_url(self, slug, type_):
		return self.base_url.format('{type}/{slug}/'.format(type=type_, slug=slug))
