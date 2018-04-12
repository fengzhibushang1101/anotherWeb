$(function () {

    function open_link(url) {
        var el = document.createElement("a");
        document.body.appendChild(el);
        el.href = url;
        el.target = "_blank";
        el.click();
        document.body.removeChild(el);
    }

    $("#begin-generate").click(function () {
        var match = location.pathname.match(/gif\/([^\\\s]+)/);
        if (!match) {
            return false;
        }
        $("#dl-link").hide();
        var _this = $(this).addClass("disabled");
        var name = match[1];
        var sentences = $(".sentence").get().map(function (d) {
            return $(d).val().trim();
        });
        $.post("/gif/generate/gif", {
            name: name,
            sentences: JSON.stringify(sentences)
        }, function (data) {
            _this.removeClass('disabled');
            if (data.status) {
                // var a = $("#trigger-a").attr({
                //     "href": location.host + '/' + data.path,
                //     "target": "_blank"
                // })[0];
                // var e = document.createEvent('MouseEvents');
                // e.initEvent('click', true, true);
                // a.dispatchEvent(e);
                // a.click();
                // var tmpwindow = window.open();
                // tmpwindow.location = location.host + '/' + data.path;
                var url = '//' + location.host + '/' + data.path;
                var tmpArr = url.split("/");
                var name = tmpArr[tmpArr.length - 1];
                // window.open(url);
                $("#dl-link").attr({
                    "href": url,
                    "download": name
                }).show();
            } else {
                alert(data.message);
            }
        })
    })
});