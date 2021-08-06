window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    document.getElementsByClassName("navbar-brand")[0].style.fontSize = "20px";
    document.getElementsByClassName("navbar-brand")[0].style.transition = ".5s";
    document.getElementsByClassName("navbar")[0].style.backgroundColor = "#066";
} else {
	document.getElementsByClassName("navbar-brand")[0].style.fontSize = "22px";
    document.getElementsByClassName("navbar-brand")[0].style.transition = ".5s";
	document.getElementsByClassName("navbar")[0].style.backgroundColor = "transparent";
  }
}