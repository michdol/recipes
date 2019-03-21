from rest_framework import generics
from rest_framework.permissions import AllowAny

from recipes.constants import RECIPE_STATUS_PUBLIC
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class RecipeList(generics.ListAPIView):
	serializer_class = RecipeSerializer
	permission_classes = (AllowAny,)

	def get_queryset(self):
		return Recipe.objects.filter(status__gte=RECIPE_STATUS_PUBLIC)
