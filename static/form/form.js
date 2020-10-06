$(function(){
  ////////////// ajax setup   /////////////////////////
    var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // Ensure jQuery AJAX calls set the CSRF header to prevent security errors
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
  });

function visibility1(self) {
  console.log(self);
  var a = document.getElementById("myinput1");
  var b = document.getElementById("hide1");
  var c = document.getElementById("hide2");

  if (a.type === "password") {
    a.type = "text";
    b.style.display = "inline";
    c.style.display = "none";
  }
  else if(a.type === "text"){
    a.type = "password";
    b.style.display = "none";
    c.style.display = "inline";
  }
}

function visibility2() {
  var x = document.getElementById("myinput2");
  var y = document.getElementById("hide3");
  var z = document.getElementById("hide4");

  if (x.type === "password") {
    x.type = "text";
    y.style.display = "inline";
    z.style.display = "none";
    }
  else if(x.type === "text" ){
    x.type = "password";
    y.style.display = "none";
    z.style.display = "inline";
  }
}

function delete_entries(){
  var checked = $('input[name="del"]:checked').map(function(){return this.value;}).get()
  let state = JSON.stringify(checked);                
  if (checked.length){  // checkes if one or more are selected or not
    console.log(state)
    $.ajax({
      type: "post",
      data: state,
      success: function (){
        location.reload(); // reload page after success of post
        console.log("hii");
      }
    });
  }
}

/*//////////////DROPDOWN//////////////*/
