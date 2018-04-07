$(function () {
    var ws = new WebSocket("ws://{0}/ws".format(location.host));
    ws.onopen = function () {
        ws.send("hello!");
    };
    ws.onmessage = function (evt) {
        var data = JSON.parse(evt.data);
        writeMessage(data);

    };
    ws.onclose = function(ev) {
        console.log(ev);
        writeMessage({
            type: 'sys',
            message: "链接断开, 请刷新页面重新链接"
        })
    };

    function writeMessage(data) {
        if (data["type"] === "sys") {
            $('#chat-content').append("<p style='width: 100%; text-align:center;'><span class='sys-mess'>" + data['message'] + "</span></p>");
        } else if (data["type"] === "self") {
             $('#chat-content').append("<p class='other-mess'>" + data['name'] + ": <br>" +"<span style='color: blue'>" + data['message'] + "</span>" + "</p>");
        } else {
             $('#chat-content').append("<p class='my-mess'>" + data['name'] + ": <br>" +"<span style='color: red'>" + data['message'] + "</span>" + "</p>");
        }
    }

    $("#send-message").click(function() {
        var content = $("#chat-text"),
            text = content.val().trim();
        if(text) {
            ws.send(text);
            content.val('');
        }
    })
});