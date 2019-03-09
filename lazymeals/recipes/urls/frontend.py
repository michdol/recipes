from django.urls import path

from recipes.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
]
