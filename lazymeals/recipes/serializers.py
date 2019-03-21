from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recipe
		fields = (
			'id', 'source', 'name', 'url', 'ingredients_json', 'directions_json', 'image_url', 'status', 'extra',
			'created', 'updated'
		)
