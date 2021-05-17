window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    document.getElementsByClassName("navbar-brand")[0].style.fontSize = "20px";
    document.getElementsByClassName("navbar-brand")[0].style.transition = ".5s";
    document.getElementsByClassName("navbar-brand")[0].style.backgroundColor = "transparent";
  } else {
    document.getElementsByClassName("navbar-brand")[0].style.fontSize = "22px";
    document.getElementsByClassName("navbar-brand")[0].style.transition = ".5s";
  }
}

var lastScrollTop = 0;
navbar = document.getElementsByClassName("navbar")[0];
window.addEventListener("scroll",function() {
  var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  if(scrollTop > lastScrollTop) {
    navbar.style.top = "-80px";
    navbar.style.transition = ".5s";
  }
  else {
    navbar.style.top = "0px";
  }
  lastScrollTop = scrollTop;
});