let tgt_url = "https://ohfish.me/api/reply/start";

function genderKor(gender){
  if(gender === '1'){
    return '남';
  }
  else if(gender === '0'){
    return '여';
  }
}

$(document).ready(function(){
    $("#info").submit(function(event){
      if (confirm("다음이 맞나요?\n\n성함: " + $("#name").val() + " (" + $("#age").val() + "세 " + genderKor($("#sex").val()) + ")\n" + 
      "학번: " + $("#no").val() +"\n연락처: " + $("#phone").val() + "\n이메일: " + $("#email").val() + "\n" )){  
        
        // payload_data = $(this).serializeArray();
        

        sessionStorage.setItem("name", $("#name").val());
        sessionStorage.setItem("age", $("#age").val());
        sessionStorage.setItem("sex", $("#sex").val());
        sessionStorage.setItem("no", $("#no").val());
        sessionStorage.setItem("phone", $("#phone").val());
        sessionStorage.setItem("email", $("#email").val());
        
        var payload = {};
        payload['name'] = sessionStorage.getItem("name");
        payload['age'] = parseInt(sessionStorage.getItem("age"));
        payload['sex'] = parseInt(sessionStorage.getItem("sex"));
        payload['no'] = sessionStorage.getItem("no");
        payload['phone'] = sessionStorage.getItem("phone");
        payload['email'] = sessionStorage.getItem("email");
        
        console.log(payload);
        $.ajax(
            {
              url: tgt_url,
              type: "POST",
              contentType:'application/json; charset= utf-8',
              data: JSON.stringify(payload),
              dataType: 'json',
              success: function(result) {
                var txt="";
                var st = 0;
                for (var x in result){
                    txt += result[x]+"\n";
                    sessionStorage.setItem(st, result[x]);
                    st++;
                }
                alert(txt);
                window.location.href = 'exp.html';
              },
              error: function(error) { alert("Bad");
              window.location.href = 'exp.html';
            }
            }
          )
        
        return false;    
      }
    }
    );
  });