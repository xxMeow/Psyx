let boxscript = '<div id="" class="box"><h3 id="title">'+ sessionStorage.getItem("fname") +'</h3><div id="boxinfo"><h4>나이 범위: ' + sessionStorage.getItem("minAge") + '세 ~ ' + sessionStorage.getItem("maxAge") + '세</h4><h4>성별: '+ sessionStorage.getItem("sex") +'</h4><h4>응답 수: 20</h4></div><div id="buttons"><button id="download_b" class="btn" onclick="download_data()">다운로드</button><br><button id="delete_b" class="btn" onclick="delete_folder()">삭제</button></div></div>';

function create_folder() {
  console.log(boxscript);
  document.getElementById('left').innerHTML += boxscript;
}

function delete_folder() {
  if(confirm("삭제할까요?")){
    document.getElementById('left').innerHTML -= boxscript;
  }
}

function download_data() {
  if(confirm("다운로드를 시작하겠습니다")){
    //다운로드 시작
  }
}

$(document).ready(function(){
  $("form").submit(function(){
    if ($("#minAge").val() > $("#maxAge").val()) {
      alert("나이를 확인해주세요!");
    }
    else if (confirm("다음 폴더를 생성할까요?\n\n폴더 이름: " + $("#fname").val() + "\n나이 범위: " + $("#minAge").val() + "세 ~ " + $("#maxAge").val() +  "세 " + "\n성별: " +
    $("#sex").val())){
      sessionStorage.clear();
      sessionStorage.setItem("fname", $("#fname").val());
      sessionStorage.setItem("minAge", $("#minAge").val());
      sessionStorage.setItem("maxAge", $("#maxAge").val());
      sessionStorage.setItem("sex", $("#sex").val());
      create_folder();
    } 
    return false;
    }
  );
});