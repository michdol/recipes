( function(window) {

    'use strict';

    window.scope = {
        recipes: [],
        last_response: null,
        has_next: false,
        initial_request: true
    }
    var sending = false;

    var main_recipes = $('#main_recipes');
    var threshold_height = document.getElementById('main_recipes').scrollHeight;
    var default_height = threshold_height;
    var current_height = null;
    main_recipes.scroll(function() {
        var el = document.getElementById('main_recipes');
        current_height = el.scrollTop + el.offsetHeight;
        //console.log(current_height, threshold_height);
        if (current_height > threshold_height) {
            threshold_height = current_height;
        }
        if (current_height >= threshold_height && !sending) {
            sending = true;
            getRecipes()
        }
    });

    function getRecipes() {
        var url = getUrl();
        if (!url) {
            return
        }
        window.ajax.get(url, '', function(err, response) {
            if (!err && response) {
                window.scope['last_response'] = response;
                window.scope['recipes'] = response.results;
            }
            else {
                console.log('error', err);
            }
        });
    }

    function getUrl() {
        if (window.scope.initial_request) {
            window.scope.initial_request = false;
            return window.ajax.api.recipes + '?page=2'
        }
        if (window.scope.has_next) {
            return window.scope.last_response.next
        }
        return null
    }

    //renderMultipleTemplates('recipe', window.scope.recipes, $('#main_recipes'));

    function watch(obj, prop, handler) {
        var currval = obj[prop];
        function callback() {
            if (obj[prop] != currval) {
                var temp = currval;
                currval = obj[prop];
                handler(temp, currval);
            }
        }
        return callback;
    }

    var myhandler = function (oldval, newval) {
        renderMultipleTemplates('recipe', window.scope.recipes, $('#main_recipes'));

        if (window.scope.last_response != null && window.scope.last_response.next != null) {
            window.scope.has_next = true
        }
        else {
            window.scope.has_next = false
        }

        setTimeout(function() {
            var el = document.getElementById('main_recipes');
            threshold_height = el.scrollHeight;
            //console.log('new threshold_height', threshold_height);
            sending = false;
        }, 1000);
    };

    var intervalH = setInterval(watch(window.scope, "recipes", myhandler), 100);

})(window);
