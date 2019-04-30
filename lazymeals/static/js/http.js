( function(window) {

    'use strict';

    var api = {
        recipes: "http://api.lazymeals.local:8000/recipes/"
    };

    var ajax = {
        api: api,
        get: get
    };

    function dataToUrl(object) {
        var encodedString = '';
        for (var prop in object) {
            if (object.hasOwnProperty(prop)) {
                if (encodedString.length > 0) {
                    encodedString += '&';
                }
                encodedString += encodeURI(prop + '=' + object[prop]);
            }
        }
        return encodedString;
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i];
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function get(url, data, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url + (data ? '?' + dataToUrl(data) : ''));
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.onload = function () {
            if (xhr.status === 200) {
                callback(null, JSON.parse(xhr.responseText));
            }
            else {
                callback(new Error('Request failed.  Returned status of ' + xhr.status));
            }
        };
        xhr.send();
    }

    window.ajax = ajax;

})(window);
