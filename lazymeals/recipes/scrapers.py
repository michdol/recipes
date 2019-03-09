import requests

from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from recipes.constants import TASTY_SOURCE_ID
from recipes.models import SourceWebsite


class TastyScrapper(object):
	def __init__(self):
		self.website_id = TASTY_SOURCE_ID
		self.website = SourceWebsite.objects.get(id=self.website_id)
		self.api_base_url = "https://tasty.co/api/{}"
		self.recent_recipes_endpoint = "recipes/recent"
		self.api_url = self.api_base_url.format(self.recent_recipes_endpoint)
		self.api_params = "size={size}&from={from}&page={page}&from_offset={from_offset}&__amp_sour"
		"https://tasty.co/api/recipes/recent?size=20&from=20&page=2&from_offset=1&__amp_s"
		"https://tasty.co/api/recipes/recent?size=20&from=40&page=3&from_offset=1&__amp_sour"
		"https://tasty.co/api/recipes/recent?size=20&from=60&page=4&from_offset=1&__amp_sour"

	def build_url(self, **params):
		return "?".join([
			self.api_url,
			self.api_params.format(**params)
		])

	def main(self):
		with requests.Session() as session:
			params = {
				"size": 20,
				"from": 20,
				"page": 1,
				"from_offset": 1
			}
			url = self.build_url(**params)
			ajax_response = session.get(url)
			# TODO: check in what format the response comes and mock it in tests
		return True

	def notes(self):
		"""
		No need for base html in case of Tasty
		Use api and combine slug in results with base url?
		https://tasty.co/recipe/{slug}
		"""
		pass
