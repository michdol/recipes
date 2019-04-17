( function(window) {

    'use strict';

    window.ajax = ajax;
    window.scope = {
        recipes: []
    }

    var main_recipes = $('#main_recipes');
    main_recipes.scroll(function() {
        var main_recipes_height = main_recipes.height();
        // console.log(main_recipes.scrollTop());
        // console.log(main_recipes.height());
        
        if (main_recipes.scrollTop() >= main_recipes_height) {
            console.log('calling api')
            ajax.getRecipes(window.scope)
        }

        if($('#main_recipes').scrollTop() + $('#main_recipes').height() == $(document).height()) {
            console.log('calling api')
            ajax.getRecipes()
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
        renderMultipleTemplates('recipe', window.scope.recipes, $('#main_recipes'));
    };

    var intervalH = setInterval(watch(window.scope, "recipes", myhandler), 100);

    // ajax.getRecipes(window.scope)
    // console.log(window.scope)

})(window);
