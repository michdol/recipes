from django.conf import settings
from subdomains.utils import reverse


def home_reverse(viewname, **kwargs):
    return reverse(viewname, subdomain=None, **kwargs)


def api_reverse(viewname, **kwargs):
    return reverse(viewname, subdomain=settings.SUBDOMAIN_API, **kwargs)
