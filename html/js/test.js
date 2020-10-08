function genderKor(gender) {
    if (gender === "1") {
        return "남";
    } else if (gender === "2") {
        return "여";
    }
}

$(document).ready(function() {
    $("#info").submit(function(event) {
        // TODO: delete this
        if (confirm("다음이 맞나요?\n\n성함: " + $("#name").val() + " (" + $("#age").val() + "세 " + genderKor($("#sex").val()) + ")\n" +
        "학번: " + $("#no").val() + "\n연락처: " + $("#phone").val() + "\n이메일: " + $("#email").val() + "\n")) {
            sessionStorage.setItem("name", $("#name").val());
            sessionStorage.setItem("age", $("#age").val());
            sessionStorage.setItem("sex", $("#sex").val());
            sessionStorage.setItem("no", $("#no").val());
            sessionStorage.setItem("phone", $("#phone").val());
            sessionStorage.setItem("email", $("#email").val());

            var payload = {};
            payload["name"] = sessionStorage.getItem("name");
            payload["age"] = parseInt(sessionStorage.getItem("age"));
            payload["sex"] = parseInt(sessionStorage.getItem("sex"));
            payload["no"] = sessionStorage.getItem("no");
            payload["phone"] = sessionStorage.getItem("phone");
            payload["email"] = sessionStorage.getItem("email");
            console.log(payload);

            $.ajax({
                url: "/api/reply/start",
                method: "POST",
                dataType: "json",
                contentType: "application/json; charset= utf-8",
                data: JSON.stringify(payload),
                success: function(data) {
                    console.log("reply start success");
                    console.log(data);
                    var txt = "";
                    var st = 0;
                    for (var x in data) {
                        txt += data[x] + "\n";
                        sessionStorage.setItem(st, data[x]);
                        st++;
                    }
                    console.log(txt); // TODO: remove this line
                    window.location.href = "testing.html";
                },
                error: function(xhr, status, error) { // alert error message
                    console.log("reply start error");
                    if (xhr.status == 400) {
                        // get popup msg from returned webpage
                        var res = $("<div></div>");
                        res.html(xhr.responseText);
                        alert($("p", res).text());
                    } else {
                        document.write(xhr.responseText);
                    }
                }
            });
            return false;
        }
    });
});