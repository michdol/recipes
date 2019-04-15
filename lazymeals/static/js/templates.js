//https://github.com/kriyeng/create-your-framework/blob/2517453544185a41b557bb8a68f7e8bcf4272fcc/with-your-framework/js/dynamic-template.js

var ROOT_URL = 'http://lazymeals.local:8000/static/partials/';

var TEMPLATE_PATHS = {
    'recipe': 'recipe.html'
};

function readTemplate(alias)
{
    var file = getTemplatePath(alias);
    var rawFile = new XMLHttpRequest();
    var allText = null;
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                allText = rawFile.responseText;
            }
        }
    };
    rawFile.send(null);
    return allText
}

function getTemplatePath(alias) {
    var path = TEMPLATE_PATHS[alias];
    console.log(path);
    if (path === undefined) {
        console.error('File not found for alias: ' + alias);
    }
    return ROOT_URL + path
}

// Usage:
// readTemplate(getTemplatePath('recipe'));

function getDynamicVariables(html_string) {
    var variables = (html_string.match(/{[\s]?[a-zA-Z0-9\.]+[\s]?}/g) || [])
    console.log(variables);
    for (var i=0; i < variables.length; i++) {
        var original = variables[i];
        var next = original.replace(/[\{\s\}]/g, '');
        var splitted = next.split('.');
        var obj_name = splitted[0];
        var property_name = splitted[1];
        var obj = window.scope[obj_name];
        var property_value = obj[property_name];
    }
}
// 1. define if it is a single variable or an object
// 2. if it is single variable -> get value from scope
// 3. if it is object -> define if it is nested property

function test() {
    var html = readTemplate('recipe');
    getDynamicVariables(html)
}