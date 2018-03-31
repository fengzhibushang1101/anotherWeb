/**
 * Created by yueqingji on 2018/3/13.
 */

var Init = (function () {

    function changeProps (el, props) {
        Object.keys(props).forEach(function (k) {
            el.setAttribute(k, props[k]);
        });
        return el;
    }

    function appendChildren (el, children) {
        children.forEach(function (child) {
            el.appendChild(child);
        });
        return el;
    }

    function createElement (tagName, props, text) {
        var el = document.createElement(tagName);
        changeProps(el, props);
        if (text) {
            var textNode = document.createTextNode(text);
            el.appendChild(textNode);
        }
        return el;
    }

    return {
        createEl: createElement,
        changeProps: changeProps,
        appendChildren: appendChildren
    }
})();