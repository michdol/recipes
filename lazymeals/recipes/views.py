from django.views.generic.base import TemplateView
from recipes.constants import RECIPE_STATUS_PUBLIC

from recipes.models import Recipe


class IndexView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["recipes"] = Recipe.objects.filter(status__gte=RECIPE_STATUS_PUBLIC)[:20]
		return context


class RecipeDetails(TemplateView):
	template_name = 'recipes/details.html'
