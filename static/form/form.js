function visibility1() {
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
