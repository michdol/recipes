from django.conf import settings
from django.contrib.sites.models import Site
from rest_framework.test import APITestCase


class ApiTestCase(APITestCase):
    DOMAIN = 'lazymeals.local'

    @classmethod
    def setUpClass(cls):
        setattr(settings, 'ALLOWED_HOSTS', '*')
        super(ApiTestCase, cls).setUpClass()

    def setUp(self):
        super(ApiTestCase, self).setUp()
        self.site = Site.objects.get_current()
        self.site.domain = self.DOMAIN
        self.site.save()
        self.client.defaults.update({
            'HTTP_HOST': 'api.{}'.format(self.DOMAIN),
            'HTTP_X_FORWARDED_PROTO': 'https',
            'HTTP_X_FORWARDED_FOR': '127.0.0.1'
        })
