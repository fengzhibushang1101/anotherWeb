(function () {
    $("#log-in").click(function () {
        $.post("/login", {
            mobile: $("#mobile").val().trim(),
            pwd: $("#pwd").val().trim()
        }).done(function (data) {
            if (data.status) {
                location.href = "/"
            } else {
                alert(data.message);
            }

        })
    });
    $("#register").click(function() {
        var mobile = $("#new-mobile").val().trim();
        var password = $("#new-pwd").val().trim();
        var password2 = $("#new-pwd2").val().trim();
        if (!mobile || !password) {
            alert("密码或者账号不能为空!");
            return;
        }
        if (password !== password2) {
            alert("两次密码不一致!");
            return;
        }
        $.post("/register", {
            mobile: mobile,
            password: password,
            password2: password2
        }).done(function (data) {
            if(data.status){
                alert("注册成功!");
                location.href = "/";
            } else {
                alert(data.message);
            }
        })
    })
})();