(function () {
    $("#log-in").click(function () {
        $.post("/login", {
            mobile: $("#mobile").val().trim(),
            pwd: $("#pwd").val().trim()
        }).done(function () {
            location.href = "/";
        })
    });
})();