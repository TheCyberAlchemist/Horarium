// $(document).ready(function() {
//     var scroll = $(document).scrollTop();
//     var navHeight = $('.navv').outerHeight();
//
//     $(window).scroll(function(){
//
//       var scrolled = $(document).scrollTop();
//
//       if(scrolled > navHeight){
//         $('.navv').addClass('animate');
//       }
//       else {
//         $('.navv').removeClass('animate');
//       }
//       if(scrolled > scroll){
//         $('.navv').removeClass('sticky');
//       }
//       else {
//         $('.navv').addClass('sticky');
//       }
//       scroll = (document).scrollTop();
//     });
//   });

  function toggle() {
    var x = document.getElementById("show_tree");
    var y = document.getElementById("show_navbar");
    if (x.style.display === "none") {
      x.style.display = "block";
      y.style.display = "none";
    } else {
      x.style.display = "none";
      y.style.display = "inline";
    }

  }
