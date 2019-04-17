var ROOT_URL = 'http://lazymeals.local:8000/';

var URLS = {
    'static': 'static/',
    'recipes': 'recipes/'
};

function reverse(alias, path) {
    url = ROOT_URL + URLS[alias]
    if (path && typeof path == 'string') {
    	url = url + path
    }
    return url
}
