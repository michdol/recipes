from django.urls import path

from recipes.views_api import RecipeList

urlpatterns = [
    path('', RecipeList.as_view(), name='recipes_list'),
]
