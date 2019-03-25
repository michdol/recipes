import json
import mock
import os

from django.test import TestCase

from recipes.constants import TASTY_SOURCE_ID
from recipes.models import Recipe
from scrapers.scrapers import TastyScrapper


class ScrapperTestMixin(object):
	scrapper_class = None
	source_id = None
	scrapper = None

	def setUp(self):
		self.scrapper = self.scrapper_class(source_id=self.source_id)


class TastyScrapperTest(ScrapperTestMixin, TestCase):
	fixtures = ('source_websites',)
	scrapper_class = TastyScrapper
	source_id = TASTY_SOURCE_ID
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

	@mock.patch("scrapers.scrapers.requests.Session", autospec=True)
	def test_main(self, mock_session):
		api_response_file = os.path.join(self.TEST_DATA_DIRECTORY, 'tasty_api_response.json')
		api_next_response_file = os.path.join(self.TEST_DATA_DIRECTORY, 'tasty_api_next_response.json')
		empty_response = {
			"aggregated_tags": [],
			"aggregations": {
				"the_name": {
					"doc_count_error_upper_bound": 0,
					"sum_other_doc_count": 0,
					"buckets": []
				}
			},
			"items": [],
			"localization": [
				None,
				None,
				"en_US"
			],
			"recipe_count": 500,
			"status": "ok"
		}
		side_effects = []

		with open(api_response_file, encoding="utf-8") as response:
			side_effects.append(json.loads(response.read()))
		with open(api_next_response_file, encoding="utf-8") as response:
			side_effects.append(json.loads(response.read()))
		side_effects.append(empty_response)
		mock_session.return_value.get.return_value.json.side_effect = side_effects
		ret = self.scrapper.main()
		self.assertTrue(ret)
		qs = Recipe.objects.all()
		self.assertEqual(qs.count(), 39)
		self.assertEqual(self.scrapper.requests_count, 3)

		recipe = qs.get(name='Kid-Friendly Fried Rice 4 Ways')
		self.assertEqual(recipe.source_id, 1)
		self.assertEqual(recipe.url, 'https://tasty.co/compilation/4-ways-to-make-fried-rice/')
		self.assertEqual(recipe.image_url, 'https://img.buzzfeed.com/video-api-prod/assets/29c929d88b3646a08c020a7a62629255/BFV24904_FriedRice4Ways_ThumbFB.jpg?output-format=webp&output-quality=60&resize=600:*')
		recipe_extra = recipe.extra
		self.assertEqual(recipe_extra.get('id'), 183)
		self.assertEqual(recipe_extra.get('tags'), 'stove_top,weeknight,easy,fusion,mixing_bowl,japanese,dry_measuring_cups,kid_friendly,measuring_spoons,one_pot_or_pan,dinner,wok,pyrex,american,liquid_measuring_cup,pan_fry,wooden_spoon')
		self.assertEqual(recipe_extra.get('type'), 'compilation')
		self.assertEqual(recipe_extra.get('object_name'), '4-ways-to-make-fried-rice')
		# This is a duplicated recipe in responses.
		self.assertIsNotNone(qs.get(name="One-Pot Ground Beef Stroganoff"))

	@mock.patch("scrapers.scrapers.requests.Session", autospec=True)
	def test_main_exception_on_request(self, mock_session):
		mock_session.return_value.get.side_effect = ValueError("mock error")
		ret = self.scrapper.main()
		self.assertFalse(ret)
		self.assertEqual(self.scrapper.requests_count, 0)

	@mock.patch("scrapers.scrapers.requests.Session", autospec=True)
	def test_main_request_limit_reached(self, mock_session):
		api_response_file = os.path.join(self.TEST_DATA_DIRECTORY, 'tasty_api_response.json')
		with open(api_response_file, encoding="utf-8") as response:
			mock_session.return_value.get.return_value.json.return_value = json.loads(response.read())
		self.scrapper.requests_count = 9

		ret = self.scrapper.main()
		self.assertTrue(ret)
		qs = Recipe.objects.all()
		self.assertEqual(qs.count(), 20)
		self.assertEqual(self.scrapper.requests_count, 10)

		recipe = Recipe.objects.get(name='Kid-Friendly Fried Rice 4 Ways')
		self.assertEqual(recipe.source_id, 1)
		self.assertEqual(recipe.url, 'https://tasty.co/compilation/4-ways-to-make-fried-rice/')
		self.assertEqual(recipe.image_url, 'https://img.buzzfeed.com/video-api-prod/assets/29c929d88b3646a08c020a7a62629255/BFV24904_FriedRice4Ways_ThumbFB.jpg?output-format=webp&output-quality=60&resize=600:*')
		recipe_extra = recipe.extra
		self.assertEqual(recipe_extra.get('id'), 183)
		self.assertEqual(recipe_extra.get('tags'), 'stove_top,weeknight,easy,fusion,mixing_bowl,japanese,dry_measuring_cups,kid_friendly,measuring_spoons,one_pot_or_pan,dinner,wok,pyrex,american,liquid_measuring_cup,pan_fry,wooden_spoon')
		self.assertEqual(recipe_extra.get('type'), 'compilation')
		self.assertEqual(recipe_extra.get('object_name'), '4-ways-to-make-fried-rice')

	def test_get_next_page_params(self):
		kwargs = {
			'size': 20,
			'from': 0,
			'page': 1,
			'from_offset': 1
		}
		ret = self.scrapper.get_next_page_params(**kwargs)
		self.assertEqual(ret.get('from'), 20)
		self.assertEqual(ret.get('page'), 2)
		self.assertEqual(ret.get('size'), 20)
		self.assertEqual(ret.get('from_offset'), 1)

		ret = self.scrapper.get_next_page_params(**ret)
		self.assertEqual(ret.get('from'), 40)
		self.assertEqual(ret.get('page'), 3)
		self.assertEqual(ret.get('size'), 20)
		self.assertEqual(ret.get('from_offset'), 1)

	def test_get_next_page_params_previous(self):
		kwargs = {
			'size': 20,
			'from': 40,
			'page': 3,
			'from_offset': 1
		}
		ret = self.scrapper.get_next_page_params(previous=True, **kwargs)
		self.assertEqual(ret.get('from'), 20)
		self.assertEqual(ret.get('page'), 2)
		self.assertEqual(ret.get('size'), 20)
		self.assertEqual(ret.get('from_offset'), 1)

		ret = self.scrapper.get_next_page_params(previous=True, **ret)
		self.assertEqual(ret.get('from'), 0)
		self.assertEqual(ret.get('page'), 1)
		self.assertEqual(ret.get('size'), 20)
		self.assertEqual(ret.get('from_offset'), 1)

	def test_get_next_page_params_previous_invalid_params(self):
		kwargs = {
			'size': 20,
			'from': 19,
			'page': 2,
			'from_offset': 1
		}
		with self.assertRaises(ValueError) as e:
			self.scrapper.get_next_page_params(previous=True, **kwargs)
		self.assertEqual(e.exception.args[0], "Invalid parameters: page - 2; from - 19")
		kwargs = {
			'size': 20,
			'from': 40,
			'page': 0,
			'from_offset': 1
		}
		with self.assertRaises(ValueError) as e:
			self.scrapper.get_next_page_params(previous=True, **kwargs)
		self.assertEqual(e.exception.args[0], "Invalid parameters: page - 0; from - 40")

	def test_parse_response(self):
		response = {'status': 'bad request'}
		with self.assertRaises(ValueError) as e:
			self.scrapper.parse_response(response)
		self.assertEqual(e.exception.args[0], 'Response status \'bad request\'')

		response = {'status': 'ok', 'recipe_count': 666}
		self.scrapper.parse_response(response)
		self.assertEqual(self.scrapper.recipe_count, 666)

	def test__create_tasty_url(self):
		url = self.scrapper._create_tasty_url('slug', 'recipe')
		self.assertEqual(url, 'https://tasty.co/recipe/slug/')
		url = self.scrapper._create_tasty_url('slug1', 'compilation')
		self.assertEqual(url, 'https://tasty.co/compilation/slug1/')

	def test_create_recipes(self):
		items = [
			{
				"name": "5 Healthy &amp; Hearty Fall Soups",
				"thumb_big": "https://img.buzzfeed.com/thumbnailer-prod-us-east-1/video-api/assets/109438.jpg?output-format=webp&output-quality=60&resize=600:*",
				"slug": "5-healthy-hearty-fall-soups",
				"object_name": "5-healthy-hearty-fall-soups",
				"id": 259,
				"type": "compilation",
				"tags": [
					"wooden_spoon",
					"comfort_food",
					"fall"
				]
			},
			{
				"name": "One-Pot Chicken Alfredo",
				"thumb_big": "https://img.buzzfeed.com/video-api-prod/assets/a2d506021b4a4256984416bd65e41274/BFV4926_One-PotChickenAlfredo-Thumb1080.jpg?output-format=webp&output-quality=60&resize=600:*",
				"slug": "one-pot-chicken-alfredo",
				"object_name": "one-pot-chicken-alfredo",
				"id": 143,
				"type": "recipe",
				"tags": [
					"american",
					"italian"
				]
			}
		]
		self.scrapper.create_recipes(items)
		qs = Recipe.objects.all()
		self.assertEqual(qs.count(), 2)
		soups = qs.get(name='5 Healthy &amp; Hearty Fall Soups')
		chicken = qs.get(name='One-Pot Chicken Alfredo')
		self.assertEqual(soups.source_id, 1)
		self.assertEqual(soups.url, 'https://tasty.co/compilation/5-healthy-hearty-fall-soups/')
		self.assertEqual(soups.image_url, 'https://img.buzzfeed.com/thumbnailer-prod-us-east-1/video-api/assets/109438.jpg?output-format=webp&output-quality=60&resize=600:*')
		soups_extra = soups.extra
		self.assertEqual(soups_extra.get('id'), 259)
		self.assertEqual(soups_extra.get('tags'), 'wooden_spoon,comfort_food,fall')
		self.assertEqual(soups_extra.get('type'), 'compilation')
		self.assertEqual(soups_extra.get('object_name'), '5-healthy-hearty-fall-soups')

		self.assertEqual(chicken.source_id, 1)
		self.assertEqual(chicken.url, 'https://tasty.co/recipe/one-pot-chicken-alfredo/')
		self.assertEqual(chicken.image_url, 'https://img.buzzfeed.com/video-api-prod/assets/a2d506021b4a4256984416bd65e41274/BFV4926_One-PotChickenAlfredo-Thumb1080.jpg?output-format=webp&output-quality=60&resize=600:*')
		chicken_extra = chicken.extra
		self.assertEqual(chicken_extra.get('id'), 143)
		self.assertEqual(chicken_extra.get('tags'), 'american,italian')
		self.assertEqual(chicken_extra.get('type'), 'recipe')
		self.assertEqual(chicken_extra.get('object_name'), 'one-pot-chicken-alfredo')
