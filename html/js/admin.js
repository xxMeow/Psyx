var pics = [];
$(document).ready(function(){

    $("#pack_folder").change(function(){
        pics = this.files;
    });
    $("#pack_info").submit(function(){
        var fd = new FormData();
        for (var i = 0; i < pics.length; i++) {
            fd.append("file", pics[i]);
        }
        fd.append('pack_name', document.forms["pack_info"]["pack_name"].value);
        fd.append('age_lower', document.forms["pack_info"]["age_lower"].value);
        fd.append('age_upper', document.forms["pack_info"]["age_upper"].value);
        fd.append('sex', document.forms["pack_info"]["sex"].value); // this value will be converted to integer at backend

        $.ajax({
            url: "https://ohfish.me/api/admin/create",
            method: "POST",
            data: fd,
            contentType: false,
            processData: false,
            cache: false,
            success: function(data){
                alert(data);
                console.log(data);
                show_packs_func();
            }
        });

        return false;
    });

    $("#template").hide();

    show_packs_func = function() {
        var packs_info = {};

        $.ajax({
            type: "get",
            dataType: "json",
            url: "https://ohfish.me/api/admin/list",
            success: function(msg){
                packs_info = msg;
                console.log(msg);

                $("#pack_info_list").find("tr").each(function(){
                    $("#ready").remove();
                });

                var data = msg["pack_list"];
                $.each(data, function(index, value){
                    var row = $("#template").clone();
                    row.find("#pack_name").text(value.pack_name);
                    row.find("#age_lower").text(value.age_lower);
                    row.find("#age_upper").text(value.age_upper);
                    row.find("#sex").text(value.sex);
                    row.find("#count").text(value.count);
                    row.find("#date").text(value.date);
                    row.find("#p_id").text(value.p_id);
                    row.attr("id","ready");
                    row.attr("display", "inline");
                    row.appendTo("#pack_info_list");
                    row.show()
                });
            }
        });
    }

    show_packs_func();

    function download_json_array(text, name, type) {
        var jsonse = JSON.stringify(text);
        var file = new Blob([jsonse], {type: "application/json"});

        var a = document.createElement('a');
            a.href = URL.createObjectURL(file);
            a.download = name;
            a.click();
    }
    
    $("#pack_info_list").on('click', '#download_btn', function(){
        var download_url = "https://ohfish.me/api/admin/report?id=";

        console.log(download_url);

        var p_id = $(this).parent().prev().text();
        console.log(p_id);

        $.ajax({
            type: "get",
            dataType: "json",
            url: download_url + p_id,
            success: function(msg){
                console.log(msg);
                download_json_array(msg, p_id+'.json','application/json');
            }
        });
    });

    $("#pack_info_list").on('click', '#delete_btn', function(){
        var delete_url = "https://ohfish.me/api/admin/remove?id=";

        var p_id = $(this).parent().prev().prev().text();
        console.log(p_id);

        $.ajax({
            type: "get",
            dataType: "json",
            url: delete_url + p_id,
            success: function(msg){
                console.log(msg);
                show_packs_func();
                alert("Pack " + p_id + " Deleted!");
            }
        });
    });
});
