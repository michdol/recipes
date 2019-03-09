from django.urls import path

from recipes.views import IndexView, RecipeDetails

app_name = 'recipes'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('details/', RecipeDetails.as_view(), name='details')
]
