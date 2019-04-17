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
    if (path === undefined) {
        console.error('File not found for alias: ' + alias);
    }
    return ROOT_URL + path
}

function renderMultipleTemplates(template_name, data, target_dom_element) {
    var html = readTemplate(template_name);
    for (var i = 0; i < data.length; i++) {
        var obj = data[i];
        var ret = applyDynamicValues(html, obj);
        console.log(ret);
        target_dom_element.append(ret);
    }
}

function applyDynamicValues(html_string, obj) {
    var variables_with_values = getDynamicVariables(html_string, obj);
    var keys = Object.keys(variables_with_values);
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var value = variables_with_values[key];
        html_string = html_string.replace(new RegExp(key, 'gm'), value);
    }
    return html_string
}

function getDynamicVariables(html_string, obj) {
    var pattern = /(?:{{[\s]?[a-zA-Z0-9\._]+[\s]?}})/gm
    var variables = (html_string.match(pattern) || [])
    var target_strings_and_values = {};
    var found_string, target_string, object_name_and_optional_properties,
        properties_names, property_value;
    for (var i = 0; i < variables.length; i++) {
        found_string = variables[i];
        target_string = found_string.replace(/[\{\s\}]/g, '');
        object_name_and_optional_properties = target_string.split('.');
        properties_names = object_name_and_optional_properties.splice(1);
        property_value = getObjectNestedValue(obj, properties_names);
        target_strings_and_values[found_string] = property_value
    }
    return target_strings_and_values
}

function getObjectNestedValue(obj, properties) {
    if (properties.length > 0) {
        var property_name = properties[0]
        var next_obj = obj[property_name];
        return getObjectNestedValue(next_obj, properties.splice(1))
    }
    else {
        return obj
    }
}
