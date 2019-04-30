from utils.subdomain import api_reverse
from utils.test import ApiTestCase


class RecipeListTest(ApiTestCase):
	fixtures = ('source_websites', 'recipes')

	def test_get(self):
		response = self.client.get(api_reverse('recipes_list'))
		results = response.data.get('results')
		self.assertEqual(len(results), 20)

		self.assertEqual(results[0].get('id'), 1)
		self.assertEqual(results[0].get('name'), 'Flavorful Egg Recipes Anyone Can Make')
		self.assertEqual(results[0].get('source'), 1)
		self.assertEqual(results[19].get('id'), 20)
		self.assertEqual(results[19].get('name'), 'Siga Tibs And Ethiopian Salad')
		self.assertEqual(results[19].get('source'), 1)
