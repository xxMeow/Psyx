var suffix = sessionStorage.getItem(2).split(",");
const PAIR = suffix.length / 2;
// Initialize array for storing answers
let answer = new Array(PAIR);
for (var a = 0; a < answer.length; a++) {
    answer[a] = new Array(4);
}
let r_time = new Array();
let i = 0;
let j = -1;
let cnt = 0;
let t = 0;

var script = ["안녕하세요, 검사에 참여해주셔서 감사합니다", "두 얼굴 사진 중에서 어느 쪽이 본인과 더 닮았는지 응답해주세요", "왼쪽 사진이 더 닮았으면 “F”를, 오른쪽 사진이면 “J”를 눌러주세요"
    , "정답은 없으므로 최대한 직감적으로 선택해주세요", "각 시행 당 제한 시간은 3초이며 총 300번의 시행을 합니다", "준비가 되셨으면 스페이스 바를 눌러 진행해주세요", "성실히 응답해주셔서 감사합니다"];

var payload = {};
payload['p_id'] = sessionStorage.getItem(0);
payload['name'] = sessionStorage.getItem("name");
payload['age'] = parseInt(sessionStorage.getItem("age"));
payload['sex'] = parseInt(sessionStorage.getItem("sex"));
payload['no'] = sessionStorage.getItem("no");
payload['phone'] = sessionStorage.getItem("phone");
payload['email'] = sessionStorage.getItem("email");
payload['answers'] = answer;


function fORj(input) {
    if (input === 70) {
        return 'f';
    }
    else if (input === 74) {
        return 'j';
    }
}

function start_test() {
    //timer
    timer = setInterval(function () {
        if (cnt > 300) {
            cnt = 0;
            trigger_f();
        }
        cnt++;
    }, 10);

    //listen to key input
    window.addEventListener("keydown", function (event) {
        if (event.keyCode === 70 || event.keyCode === 74) {
            trigger_t();
        }
    });
}

function after() {
    //If test is done
    if (i === PAIR - 1) {
        document.getElementById("selection").classList.add('hidden');
        document.getElementById("instruction").classList.remove('hidden');
        //send answer
        console.log(answer);
        console.log(payload);
        clearInterval(timer);
        $.ajax({
            url: "https://ohfish.me/api/reply/submit",
            method: "POST",
            dataType: 'json',
            contentType: 'application/json; charset= utf-8',
            data: JSON.stringify(payload),
            success: function (result) {
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
    i++;
    // show plus
    document.getElementById("selection").classList.add('hidden');
    document.getElementById("plus").classList.remove('hidden');
    setTimeout(function () {
        document.getElementById("plus").classList.add('hidden');
        document.getElementById("selection").classList.remove('hidden');
    }, 1000);
    // load next imgs
    right = "https://ohfish.me" + sessionStorage.getItem(1) + "/" + suffix[2 * i];
    left = "https://ohfish.me" + sessionStorage.getItem(1) + "/" + suffix[2 * i + 1];
    document.getElementById("ori").src = left;
    document.getElementById("inv").src = right;
    // initialize timer 
    cnt = 0;
}

function trigger_t() {
    answer[i][0] = fORj(event.keyCode);
    answer[i][1] = cnt / 100;
    answer[i][3] = suffix[2 * i];
    answer[i][2] = suffix[2 * i + 1];
    after();
}

function trigger_f() {
    answer[i][0] = null;
    answer[i][1] = 3.00;
    answer[i][3] = suffix[2 * i];
    answer[i][2] = suffix[2 * i + 1];
    after();
}

function instruct() {
    window.addEventListener('keydown', function (event) {
        if (event.keyCode === 32 && j < script.length - 2) {
            j++;
            document.getElementsByTagName("h2")[0].remove();
            var para = document.createElement("h2");
            var node = document.createTextNode(script[j]);
            para.appendChild(node);

            var element = document.getElementById("instruction");
            element.appendChild(para);

        }
        else if (event.keyCode === 32 && j === script.length - 2) {
            document.getElementById("instruction").classList.add('hidden');
            document.getElementById("selection").classList.remove('hidden');
            var right = "https://ohfish.me" + sessionStorage.getItem(1) + "/" + suffix[2 * i];
            var left = "https://ohfish.me" + sessionStorage.getItem(1) + "/" + suffix[2 * i + 1];
            document.getElementById("ori").src = left;
            document.getElementById("inv").src = right;
            j++;
            document.getElementsByTagName("h2")[0].remove();
            var para = document.createElement("h2");
            var node = document.createTextNode(script[j]);
            para.appendChild(node);

            var element = document.getElementById("instruction");
            element.appendChild(para);
            start_test();
        }
    });
}

instruct();