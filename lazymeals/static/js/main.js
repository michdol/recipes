( function(window) {

    'use strict';
    var ajax = {
        get : get,
        getRecipes: getRecipes,
        getCookie: getCookie,
        testGet: testGet
    };

    var api = {
        recipes: "http://api.lazymeals.local:8000/recipes/"
    };

    function get(url, data, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url + (data ? '?' + dataToUrl(data) : ''));
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

    function getRecipes() {
        ajax.testGet(api.recipes, '', function(err, results) {
            if (!err && results) {
                console.log('res', results);
            }
            else {
                console.log('error', err);
            }
        });
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

    function testGet(url, data, callback) {
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

    

    var main_recipes = $('#main_recipes');
    main_recipes.scroll(function() {
        var main_recipes_height = main_recipes.height();
       console.log(main_recipes.scrollTop());
       console.log(main_recipes.height());

       if (main_recipes.scrollTop() >= main_recipes_height) {
           console.log('asd')
       }

        // if($('#main_recipes').scrollTop() + $('#main_recipes').height() == $(document).height()) {
       //     alert("bottom!");
       // }
    });

    window.ajax = ajax;
    window.scope = {
        recipe: {
            url: 'https://url.jp/',
            image_url: 'https://www.petmd.com/sites/default/files/petmd-kitten-development.jpg',
            name: 'recipe name',
            inner: {
                id: 666
            }
        },
        recipes: [
            {
                url: 'https://url.jp/',
                image_url: 'https://www.petmd.com/sites/default/files/petmd-kitten-development.jpg',
                name: 'kitten',
                inner: {
                    id: 666
                }
            },
            {
                url: 'https://url.jp/',
                image_url: 'https://www.gettyimages.com/gi-resources/images/500px/983794168.jpg',
                name: 'fisherman',
                inner: {
                    id: 666
                }
            }
        ]
    }
    //console.log(readTemplate('recipe'));
    renderMultipleTemplates('recipe', window.scope.recipes, $('#main_recipes'));

})(window);
