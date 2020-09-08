const PAIR = 5;
let answer = new Array();
let r_time = new Array();
let i = 0;
let j = -1;
let cnt = 0;
let t = 0;

var script = ["안녕하세요, 검사에 참여해주셔서 감사합니다", "두 얼굴 사진 중에서 어느 쪽이 본인과 더 닮았는지 응답해주세요", "왼쪽 사진이 더 닮았으면 “F”를, 오른쪽 사진이 더 닮았으면 “J”를 눌러주세요"
, "정답은 없으므로 최대한 직감적으로 선택해주세요", "각 시행 당 제한 시간은 3초이며 총 300번의 시행을 합니다", "준비가 되셨으면 스페이스 바를 눌러 진행해주세요", "실험에 참여해주셔서 감사합니다"];


function start_test(){
    //timer
    timer = setInterval(function(){
        if(cnt>30){
            cnt = 0;
            trigger_f();
        }
        cnt++;
    }, 100);

    //listen to key input
    window.addEventListener("keydown", function(event){
        if(event.keyCode === 70 || event.keyCode === 74) {
            trigger_t();
        }
    });
}

function after() {
    //If test is done
    if(i === PAIR - 1){
        document.getElementById("selection").classList.add('hidden');
        document.getElementById("instruction").classList.remove('hidden');
        //send answer
        console.log(answer);
        console.log(r_time);
        clearInterval(timer);
        return 0;
    }
    i++;
    // show plus
    document.getElementById("selection").classList.add('hidden');
    document.getElementById("plus").classList.remove('hidden');
    setTimeout(function(){
        document.getElementById("plus").classList.add('hidden');
        document.getElementById("selection").classList.remove('hidden');
    }, 1000);
    // load next imgs
    document.getElementById("ori").src= "img/animal/00" + (i+1) + "_ori.jpg";
    document.getElementById("inv").src= "img/animal/00" + (i+1) + "_inv.jpg";
    // initialize timer 
    cnt = 0;
}

function trigger_t() {
    answer[i] = event.keyCode;
    r_time[i] = cnt/10;
    after();
}

function trigger_f() {
    answer[i] = null;
    r_time[i] = 3.0;
    after();
}

window.addEventListener('keydown', function(event)
{
    if (event.keyCode ===32 && j < script.length - 2)
    {
        j++;
        document.getElementsByTagName("h2")[0].remove();
        var para = document.createElement("h2");
        var node = document.createTextNode(script[j]);
        para.appendChild(node);

        var element = document.getElementById("instruction");
        element.appendChild(para);
        
    }
    else if(event.keyCode ===32 && j === script.length -2){
        document.getElementById("instruction").classList.add('hidden');
        document.getElementById("selection").classList.remove('hidden');
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