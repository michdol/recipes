from django.conf.urls import include
from django.urls import path

urlpatterns = [
	path('api-auth/', include('rest_framework.urls')),
	path('recipes/', include('recipes.urls.api')),
]
