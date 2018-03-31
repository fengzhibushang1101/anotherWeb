/**
 * Created by yueqingji on 2018/3/14.
 */



_  = (function () {
    function bind(fn, obj) {
        return function () {
            var args = Array.prototype.slice.call(arguments);
            return fn.apply(fn, obj);
        }
    }
    function debounce(fn, time) {
        var timeoutId = 0;
        return function () {
            if(timeoutId) clearTimeout(timeoutId);
            var args = arguments;
            var _this = this;
            timeoutId = setTimeout(function () {
                fn.apply(_this, args);
                timeoutId = 0;
            }, time)
        }
    }

    function throttle(fn, time) {
        var outId = 0;
        return function () {
            if (!outId) {
                fn.apply(this, arguments);
                outId = setTimeout(function () {
                    outId = 0;
                }, time);
            }
        }
    }
    return {
        bind: bind,
        debounce: debounce,
        throttle: throttle
    }
}());