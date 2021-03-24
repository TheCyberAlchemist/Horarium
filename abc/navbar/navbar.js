$(document).ready(function() {
    var scroll = $(document).scrollTop();
    var navHeight = $('.navv').outerHeight();

    $(window).scroll(function(){

      var scrolled = $(document).scrollTop();

      if(scrolled > navHeight){
        $('.navv').addClass('animate');
      }
      else {
        $('.navv').removeClass('animate');
      }
      if(scrolled > scroll){
        $('.navv').removeClass('sticky');
      }
      else {
        $('.navv').addClass('sticky');
      }
      scroll = (document).scrollTop();
    });
  });
