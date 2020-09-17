$(document).ready(function() {
    function refresh_list() { // get the lastest pasks info
        $.ajax({
            type: "get",
            dataType: "json",
            url: "https://ohfish.me/api/admin/list",
            success: function(data){
                console.log(data);

                // clear old rows
                $("#pack_list").find(".old").each(function() {
                    $(this).remove();
                });

                // generate new rows from received data
                var tb = $("#pack_list").find("tbody")[0];
                if (data["pack_num"] > 0) {
                    var tplt = document.querySelector("#row_tplt");
                    var tds = tplt.content.querySelectorAll("td");
                    $.each(data["pack_list"], function(index, value){
                        // make content for template
                        tds[0].textContent = value.pack_name;
                        if (value.sex == "1") {
                            tds[1].textContent = "남";
                        } else if (value.sex == "2") {
                            tds[1].textContent = "여";
                        } else {
                            console.log("Unknown Sex.");
                        }
                        tds[2].textContent = value.age_lower;
                        tds[3].textContent = value.age_upper;
                        tds[4].textContent = value.count;
                        tds[5].textContent = value.date;
                        tds[6].textContent = value.p_id;
                        // instantiate a new row and insert it
                        var clone = document.importNode(tplt.content, true);
                        tb.appendChild(clone);
                    });
                } else {
                    // instantiate the empty row and insert it
                    var tplt = document.querySelector("#empty_row_tplt");
                    var clone = document.importNode(tplt.content, true);
                    tb.appendChild(clone);
                }

                // set the total number of packs
                $("#pack_list").find("tfoot").find("td").text(data["pack_num"]);
            }
        });
    }
    function download(data, p_id) {
        var json_str = JSON.stringify(data);
        var filename = p_id + ".json"; // use "p_id.json" to name the file
        var file = new Blob([json_str], {type: "application/json"});

        var a = document.createElement('a');
        a.href = URL.createObjectURL(file);
        a.download = filename;
        a.click();
    }

    refresh_list();

    // add new pack
    var pack_folder = [];
    $("#pack_folder").change(function() { // get files to upload
        pack_folder = this.files;
    });
    $("#new_pack_form").submit(function() {
        var fd = new FormData(); // put files into formdate
        for (var i = 0; i < pack_folder.length; i++) {
            fd.append("file", pack_folder[i]);
        }
        // put other pack info to it, too
        fd.append('pack_name', document.forms["new_pack_form"]["pack_name"].value);
        fd.append('age_lower', document.forms["new_pack_form"]["age_lower"].value);
        fd.append('age_upper', document.forms["new_pack_form"]["age_upper"].value);
        fd.append('sex', document.forms["new_pack_form"]["sex"].value); // this value will be converted to integer at backend
        // start loading animation
        $(".loader").css("visibility", "visible");
        $.ajax({
            url: "https://ohfish.me/api/admin/create",
            method: "POST",
            data: fd,
            contentType: false,
            processData: false,
            cache: false,
            success: function(data) {
                $('#new_pack_form')[0].reset(); // clear the form
            },
            complete: function(request, data) {
                $(".loader").css("visibility", "hidden"); // end loading
                console.log(data);
                alert(data);
                refresh_list();
            }
        });
        return false;
    });

    // download
    $("#pack_list").on("click", ".download_btn", function() {
        var p_id = $(this).parent().prev().text();
        console.log("Downloading Pack" + p_id + "..");

        $.ajax({
            type: "get",
            dataType: "json",
            url: "https://ohfish.me/api/admin/report?id=" + p_id,
            success: function(data){
                console.log(data);
                download(data, p_id);
            }
        });
    });

    // delete
    $("#pack_list").on("click", ".delete_btn", function() {
        var p_id = $(this).parent().prev().text();
        console.log("Deleting Pack" + p_id + "..");

        var msg = "세트 삭제 후 북구할 수 없으며 해당 세트의 모든 응답도 삭제됩니다.\n정말 삭제하시겠습니까?";
        if (confirm(msg) != true) {
            return false;
        }

        $.ajax({
            type: "get",
            dataType: "json",
            url: "https://ohfish.me/api/admin/remove?id=" + p_id,
            success: function(data){
                console.log(data);
                refresh_list();
                alert("Pack " + p_id + " Deleted!");
            }
        });
    });
});
