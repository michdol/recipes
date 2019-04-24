( function(window) {

    'use strict';

    window.ajax = ajax;
    window.scope = {
        recipes: []
    }
    var sending = false;

    var main_recipes = $('#main_recipes');
    var threshold_height = document.getElementById('main_recipes').scrollHeight;
    var default_height = threshold_height;
    var current_height = null;
    main_recipes.scroll(function() {
        // console.log(main_recipes.scrollTop());
        // console.log(main_recipes.height());
        var el = document.getElementById('main_recipes');
        current_height = el.scrollTop + el.offsetHeight;
        console.log(current_height, threshold_height);
        if (current_height > threshold_height) {
            threshold_height = current_height;
        }
        if (current_height >= threshold_height && !sending) {
            console.log('calling api 1');
            sending = true;
            ajax.getRecipes(window.scope)
        }

        if($('#main_recipes').scrollTop() + $('#main_recipes').height() == $(document).height()) {
            console.log('calling api 2')
            //ajax.getRecipes()
        }
    });

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
        console.log('handler after api call')
        renderMultipleTemplates('recipe', window.scope.recipes, $('#main_recipes'));

        setTimeout(function() {
            var el = document.getElementById('main_recipes');
            threshold_height = el.scrollHeight;
            console.log('new threshold_height', threshold_height);
            sending = false;
        }, 1000);
    };

    var intervalH = setInterval(watch(window.scope, "recipes", myhandler), 100);

    // ajax.getRecipes(window.scope)
    // console.log(window.scope)

})(window);
