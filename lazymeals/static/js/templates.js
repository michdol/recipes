//https://github.com/kriyeng/create-your-framework/blob/2517453544185a41b557bb8a68f7e8bcf4272fcc/with-your-framework/js/dynamic-template.js

var ROOT_URL = 'http://lazymeals.local:8000/static/partials/';

var TEMPLATE_PATHS = {
    'recipe': 'test.html'
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
// readTemplate(getTemplatePath('test'));
