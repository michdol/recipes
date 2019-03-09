import json
import mock
import os

from django.test import TestCase

from recipes.scrapers import TastyScrapper


class ScrapperTestMixin(object):
	scrapper_class = None

	def setUp(self):
		self.scrapper = self.scrapper_class()


class TastyScrapperTest(ScrapperTestMixin, TestCase):
	fixtures = ('source_websites',)
	scrapper_class = TastyScrapper
	TEST_DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_data/')

	def test_build_url(self):
		params = {
			"size": 20,
			"from": 20,
			"page": 1,
			"from_offset": 1
		}
		url = self.scrapper.build_url(**params)
		expected = "https://tasty.co/api/recipes/recent?size=20&from=20&page=1&from_offset=1&__amp_sour"
		self.assertEqual(url, expected)

	@mock.patch("recipes.scrapers.requests.Session.get", autospec=True)
	def test_test(self, mock_get):
		api_response_file = os.path.join(self.TEST_DATA_DIRECTORY, 'tasty_api_response.json')
		with open(api_response_file, 'r') as response:
			mock_get.return_value = response.read()
		self.scrapper.main()
