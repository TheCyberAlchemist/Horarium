window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    document.getElementById("navbar-brand").style.fontSize = "20px";
    document.getElementById("navbar-brand").style.transition = ".5s";
    document.getElementById("navbar-brand").style.backgroundColor = "transparent";
  } else {
    document.getElementById("navbar-brand").style.fontSize = "25px";
    document.getElementById("navbar-brand").style.transition = ".5s";
    document.getElementById("navbar-brand").style.backgroundColor = "#333";
  }
}