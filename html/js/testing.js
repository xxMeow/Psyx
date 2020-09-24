// turn these 2 flags to be true when pics loaded
var left_ready = false;
var right_ready = false;

// get the path prefix before beginning to save time
var pack_path = 'https://ohfish.me/' + sessionStorage.getItem(1) + '/';

// Initialize array for storing answers
const PAIR_NUM = 300;
var answers = new Array(PAIR_NUM);

const TIME_LIMIT = 3000; // 3sec = 3000ms
let start_time; // the start time of each answer
let timer; // timer for timeout
let pair_i = 0; // index of current pic pairs

let reply = {}; // read personal info from the storage

/*
TODO:
 - check left and right!
 - check th usage of var and let
*/

function submit_reply() {
    $.ajax({
        url: "https://ohfish.me/api/reply/submit",
        method: "POST",
        dataType: 'text', // TODO: text? how about other response?
        contentType: 'application/json; charset= utf-8',
        data: JSON.stringify(reply),
        success: function(result) {
            var txt = "";
            for (var x in result) {
                txt += result[x]
            }
            alert(txt);
        },
        error: function(xhr, status, error) {
            console.log("reply submit error");
            console.log(xhr);
            alert(xhr.responseText);
        }
    })

    return 0;
}

let play_sound = function() {} // declaration

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
            $("#ori").attr('src', src_left);
            $("#inv").attr('src', src_right);
        } else {
            alert('Test End!');
            submit_reply();
        }
    }, TIME_LIMIT);

    console.log('Listening.. ' + pair_i);
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
    let sounds = $('.wavsound'); // the pool
    let sound_i = 0; // index
    play_sound = function() { // recycle all the files 
        console.log(sounds.length);
        sounds[sound_i].play();
        sound_i ++;
        if (sound_i >= POOL_SIZE) {
            sound_i = 0;
        }
    }

    // guide text
    const GUIDANCE = [
        "안녕하세요, 검사에 참여해주셔서 감사합니다",
        "두 얼굴 사진 중에서 어느 쪽이 본인과 더 닮았는지 응답해주세요",
        "왼쪽 사진이 더 닮았으면 “F”를, 오른쪽 사진이면 “J”를 눌러주세요",
        "정답은 없으므로 최대한 직감적으로 선택해주세요",
        "각 시행 당 제한 시간은 3초이며 총 300번의 시행을 합니다",
        "준비가 되셨으면 스페이스 바를 눌러 진행해주세요",
        "성실히 응답해주셔서 감사합니다"
    ];
    let guidance_i = 0; // the index of sentences

    // get pic files
    let pairs = sessionStorage.getItem(2).split(",");
    if (pairs.length / 2 != PAIR_NUM) { // check for the number of them
        alert('Pack Damaged!');
    }

    // fill the answers with default value before starting to save time
    for (let i = 0; i < PAIR_NUM; i ++) {
        answers[i] = new Array(4);
        answers[i][0] = ' ';
        answers[i][1] = 3;
        answers[i][2] = pairs[i * 2];
        answers[i][3] = pairs[i * 2 + 1];
    }

    reply['p_id'] = sessionStorage.getItem(0);
    reply['name'] = sessionStorage.getItem("name");
    reply['age'] = parseInt(sessionStorage.getItem("age"));
    reply['sex'] = parseInt(sessionStorage.getItem("sex"));
    reply['no'] = sessionStorage.getItem("no");
    reply['phone'] = sessionStorage.getItem("phone");
    reply['email'] = sessionStorage.getItem("email");
    reply['answers'] = answers;

    // add the input listener
    window.addEventListener('keyup', function(event) {
        if (event.keyCode == 32 && guidance_i <= GUIDANCE.length) { // 32=SPACE
            play_sound(); // play sound for pressed space bar
            if (guidance_i == GUIDANCE.length) { // hide guide text and start test
                $("#instruction").hide();

                let src_right = pack_path + answers[0][2];
                let src_left = pack_path + answers[0][2];
                $("#ori").attr('src', src_left);
                $("#inv").attr('src', src_right);
            } else { // show guide text
                document.getElementsByTagName("h2")[0].remove();
                let para = document.createElement("h2");
                let node = document.createTextNode(GUIDANCE[guidance_i]);
                para.appendChild(node);

                let element = document.getElementById("instruction");
                element.appendChild(para);
            }
            guidance_i ++;
        } else if (left_ready && right_ready) { // only accept input when pics loaded
            if (event.keyCode == 70 || event.keyCode == 74) { // 70=F, 74=J
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
                    answers[pair_i][0] = 'F';
                } else {
                    answers[pair_i][0] = 'J';
                }
                answers[pair_i][1] = interval / 1000; // trans the ms to sec
                // get the next pair
                pair_i ++;
                if (pair_i < PAIR_NUM) {
                    let src_right = pack_path + answers[pair_i][2];
                    let src_left = pack_path + answers[pair_i][3];
                    $("#ori").attr('src', src_left);
                    $("#inv").attr('src', src_right);
                } else {
                    alert('Test End!');
                    // TODO: close page?
                    submit_reply()
                }
            }
        }
    });
});
