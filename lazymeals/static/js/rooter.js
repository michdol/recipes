var ROOT_URL = 'http://lazymeals.local:8000/';

var URLS = {
    'static': 'static/'
};

var ROOT_URL = 'http://lazymeals.local:8000/static/partials/';

function reverse(alias) {
    return ROOT_URL + URLS[alias]
}
