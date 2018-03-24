

(function () {
    // 扩展format
    String.prototype.format= function(){var args = arguments;return this.replace(/\{(\d+)\}/g,function(s,i){return args[i]})};
    // 退出
    $("#log-out").click(function() {
        $.post("/logout").done(function() {
            location.href="/";
        })
    })
})();