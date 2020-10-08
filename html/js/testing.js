// get the path prefix before beginning to save time
var pack_path = sessionStorage.getItem(1) + "/";

// turn these 2 flags to be true when pics loaded
var left_ready = false;
var right_ready = false;

// guide text
const GUIDANCE = [
    "<h2>안녕하세요, 검사에 참여해주셔서 감사합니다.</h2>",
    "<h2>두 얼굴 사진 중에서 어느 쪽이 본인과 더 닮았는지 응답해주세요.</h2>",
    "<h2>왼쪽 사진이 더 닮았으면 “F”를, 오른쪽 사진이면 “J”를 눌러주세요.</h2>",
    "<h2>정답은 없으므로 최대한 직감적으로 선택해주세요.</h2>",
    "<h2>각 시행 당 제한 시간은 3초이며 총 300번의 시행을 합니다.</h2>",
    "<h2>준비가 되셨으면 스페이스바를 눌러 진행해주세요.</h2><br /><h4> * 각 시행은 3초이후 자동으로 넘어갑니다. 최대한 빠르게 응답해주세요.<h4>",
    "<h2>성실히 응답해주셔서 감사합니다.</h2>"
];
var guidance_i = 0; // the index of sentences

// initialize array for storing answers
const PAIR_NUM = 300;
var answers = new Array(PAIR_NUM);
var pair_i = 0; // index of current pic pairs

// count time for each pair
const TIME_LIMIT = 3000; // 3sec = 3000ms
var start_time; // the start time of each answer
var timer; // timer for timeout

var reply = {}; // includes personal info and answers

/*
TODO:
 - clear debug printing
*/

function submit_reply() {
    $.ajax({
        url: "/api/reply/submit",
        method: "POST",
        dataType: "text",
        contentType: "application/json; charset= utf-8",
        data: JSON.stringify(reply),
        success: function(msg) {
            console.log("reply submit success");
            // console.log(msg);
        },
        error: function(xhr, status, error) {
            console.log("reply submit error");
            if (xhr.status == 400) {
                // get popup msg from returned webpage
                var res = $("<div></div>");
                res.html(xhr.responseText);
                alert($("p", res).text());
            } else {
                document.write(xhr.responseText);
            }
        }
    })

    return 0;
}


var goback_timer = 5;
function end() { // submit reply > show the last guidance > back to homepage
    submit_reply();
    $("#instruction").find("#sentence").html(GUIDANCE[guidance_i]);
    $("#instruction").find("img").remove()
    $("#instruction").show();

    $("#goback_timer").show();
    setInterval(function() {
        $("#goback_timer").text(goback_timer + "초 뒤에 홈페이지로 돌아가겠습니다.");
        goback_timer --;
    }, 1000);

    setTimeout(function() { // back to home page after 3sec
        window.location.href = "index.html";
    }, 5000);
}

var play_sound = function() {} // declare first so it can be used by different functions

function start_timing() {
    // the two pics will be shown at the same time they be loaded
    $("#selection").show();

    // count for 3 sec
    timer = setTimeout(function() { // this timeout function should act same way as getting input
        // disable input
        left_ready = false;
        right_ready = false;

        // hide current pics and play sound
        $("#selection").hide();
        play_sound();

        // load the next pair
        pair_i ++;
        if (pair_i < PAIR_NUM) {
            // set new src and start loading
            let src_right = pack_path + answers[pair_i][2];
            let src_left = pack_path + answers[pair_i][3];
            $("#ori").attr("src", src_left);
            $("#inv").attr("src", src_right);
        } else {
            end();
        }
    }, TIME_LIMIT);

    console.log(pair_i);
    start_time = (new Date()).getTime(); // start to count time (the timer cant be used to do this job =_=..)
}

var left_loaded = function() {
    left_ready = true;
    if (right_ready == true) { start_timing(); }
}
var right_loaded = function() {
    right_ready = true;
    if (left_ready == true) { start_timing(); }
}


$(document).ready(function() {
    // the number of audio files in the pool (otherwise the browser will download them again and again)
    const POOL_SIZE = 5;
    let sounds = $(".wavsound"); // the pool
    let sound_i = 0; // index
    play_sound = function() { // recycle all the files
        sounds[sound_i].play();
        sound_i ++;
        if (sound_i >= POOL_SIZE) {
            sound_i = 0;
        }
    }

    // get pic files
    let pairs = sessionStorage.getItem(2).split(",");

    // fill the answers with default value before starting to save time
    for (let i = 0; i < PAIR_NUM; i ++) {
        answers[i] = new Array(4);
        answers[i][0] = " ";
        answers[i][1] = 3;
        answers[i][2] = pairs[i * 2];
        answers[i][3] = pairs[i * 2 + 1];
    }

    reply["p_id"] = sessionStorage.getItem(0);
    reply["name"] = sessionStorage.getItem("name");
    reply["age"] = parseInt(sessionStorage.getItem("age"));
    reply["sex"] = parseInt(sessionStorage.getItem("sex"));
    reply["no"] = sessionStorage.getItem("no");
    reply["phone"] = sessionStorage.getItem("phone");
    reply["email"] = sessionStorage.getItem("email");
    reply["answers"] = answers;

    // add the input listener
    var is_started = false;
    window.addEventListener("keyup", function(event) {
        if (event.keyCode == 32 && guidance_i <= GUIDANCE.length) { // 32=SpaceBar
            if (guidance_i < GUIDANCE.length - 1) {
                play_sound();
                $("#instruction").find("#sentence").html(GUIDANCE[guidance_i]);
                guidance_i ++;
            } else if (is_started == false) { // spacebar can only be pressed before starting
                play_sound();
                $("#instruction").hide();

                // load the first pair
                let src_right = pack_path + answers[0][2];
                let src_left = pack_path + answers[0][3];
                $("#ori").attr("src", src_left);
                $("#inv").attr("src", src_right);

                // mark the starting
                is_started = true;
            }
        } else if (left_ready && right_ready) { // only accept input when pics loaded
            if (event.keyCode == 70 || event.keyCode == 74) { // 70=F, 74=J TODO: check for keyCode
                let interval = (new Date()).getTime() - start_time; // get time first
                // disable input
                left_ready = false;
                right_ready = false;
                clearTimeout(timer);

                // play sound and hide pics
                play_sound();
                $("#selection").hide();

                // set input as answer
                if (event.keyCode == 70) {
                    answers[pair_i][0] = "F";
                } else {
                    answers[pair_i][0] = "J";
                }
                 // trans the ms to sec
                answers[pair_i][1] = (interval / 1000).toFixed(2);

                // get the next pair
                pair_i ++;
                if (pair_i < PAIR_NUM) {
                    let src_right = pack_path + answers[pair_i][2];
                    let src_left = pack_path + answers[pair_i][3];
                    $("#ori").attr("src", src_left);
                    $("#inv").attr("src", src_right);
                } else {
                    end();
                }
            }
        }
    });
});
