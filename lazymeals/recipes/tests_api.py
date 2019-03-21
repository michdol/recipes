from recipes.models import Recipe, SourceWebsite
from utils.subdomain import api_reverse
from utils.test import ApiTestCase


class ASD(ApiTestCase):
	def test_test(self):
		s = SourceWebsite.objects.create(name='asd', url='asdasd')
		r = Recipe.objects.create(name='asd', source_id=s.id, status=9)
		response = self.client.get(api_reverse('recipes_list'))
		results = response.data
		self.assertEqual(len(results), 1)
		self.assertEqual(results[0].get("name"), r.name)
