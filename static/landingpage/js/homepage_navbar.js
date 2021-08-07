window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    document.getElementsByClassName("navbar-brand")[0].style.fontSize = "20px";
    document.getElementsByClassName("navbar-brand")[0].style.transition = ".5s";
    document.getElementsByClassName("navbar")[0].style.backgroundColor = "#066";
<<<<<<< HEAD
	document.getElementsByClassName("navbar")[0].style.transition = ".5s";
=======
>>>>>>> 540346c22d2493fe8a56114680a1a2a6b4d1d0cc
} else {
	document.getElementsByClassName("navbar-brand")[0].style.fontSize = "22px";
    document.getElementsByClassName("navbar-brand")[0].style.transition = ".5s";
	document.getElementsByClassName("navbar")[0].style.backgroundColor = "transparent";
<<<<<<< HEAD
	document.getElementsByClassName("navbar")[0].style.transition = ".5s";
=======
>>>>>>> 540346c22d2493fe8a56114680a1a2a6b4d1d0cc
  }
}