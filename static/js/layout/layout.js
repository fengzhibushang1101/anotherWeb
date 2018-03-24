

(function () {
    $("#log-out").click(function() {
        $.post("/logout").done(function() {
            location.href="/";
        })
    })
})();