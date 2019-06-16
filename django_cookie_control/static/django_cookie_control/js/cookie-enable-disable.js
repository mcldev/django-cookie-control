
// Replicates this functionality - https://cookie-script.com/how-to-block-third-party-cookies.html

var cookieAttrs = [
    ['data-src', 'src', null, null],
    ['data-href', 'href', null, null],
    ['type', 'type', 'text/plain', 'text/javascript']
];

function enableCookies(attrPrefix) {
    switchCookies(attrPrefix, true);
}

function disableCookies(attrPrefix) {
    switchCookies(attrPrefix, false);
}

function switchCookies(attrPrefix, enable) {
    // Cookie selector e.g. '[marketing-]cookie-control'
    if (typeof (attrPrefix) === 'undefined') {
        attrPrefix = '';
    }
    var selector = attrPrefix + 'cookie-control';

    // Enable or disable cookie elements
    if (typeof (enable) === 'undefined') {
        enable = false;
    }

    var cookieControls = document.querySelectorAll('[' + selector + ']');
    fromAttr = enable ? 0 : 1;
    toAttr = enable ? 1 : 0;
    fromVal = enable ? 2 : 3;
    toVal = enable ? 3 : 2;
    enableStr = enable ? 'Enabling' : 'Disabling';
    cookieControls.forEach(function (cookieElem) {
        cookieAttrs.forEach(function (cookieAttr) {
            // For iframe/embed/object with data-src
            if (cookieElem.hasAttribute(cookieAttr[fromAttr])) {
                console.log(enableStr + " content for: " + cookieElem.getAttribute(cookieAttr[fromAttr]));
                var from_attr = cookieAttr[fromAttr];
                var to_attr = cookieAttr[toAttr];
                var to_val = cookieAttr[toVal] ? cookieAttr[toVal] : cookieElem.getAttribute(from_attr);
                cookieElem.setAttribute(to_attr, to_val);
                cookieElem.removeAttribute(from_attr);
            }
        });

    });
}
