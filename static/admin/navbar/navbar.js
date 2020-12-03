// function toggle() {
//     var x = document.getElementById("show_tree");
//     var y = document.getElementById("show_navbar");
//     var z = document.getElementById("whole_container_id");
//     if (x.style.display === "none") {
//       x.style.display = "block";
//       y.style.display = "none";
//       z.style.display = "none";
//     } else {
//       x.style.display = "none";
//       y.style.display = "inline";
//       z.style.display = "block";
//     }
//   }
$(document).ready(function(){
  /////////////////////// Navbar Animation //////////////////////
  $(".wrapper").animate({height:"0%",},200);
  offset = l.offset();
  $(".me").click(function(){
    $("#whole_container_id").css({"height":"0%","width":"0%","transition":".3s"});
    $('.wrapper').animate({
          scrollTop: offset.top,
          scrollLeft: offset.left/1.5,
      }, 0);
    $(".wrapper").animate({height:'100%'},300);
    $(".wrapper").animate({height:'95%'},250);
    $(".wrapper").animate({height:'100%'},200);
    $(".wrapper").animate({height:'98%'},100);
    $(".wrapper").animate({height:'100%'},100);
    $(".wrapper").animate({height:'99%'},80);
    $(".wrapper").animate({height:'100%'},70);
    //$(".toggle_button").css({"height":"40px","width":"50px"});
    $(".toggle_button").animate({height:'40px',width:'50px'},10);
    $("fieldset").hide();
    $(".table_container").hide();
    $(".nav_container").hide();
      //$(".nav_container").animate({width:'0%',height:'0%'},100);
  });
  
  $(".not_me").click(function(){
    $(".toggle_button").css({"height":"0px","width":"0px"});
    $(".wrapper").animate({height:'0%'},400);
    $("#whole_container_id").css({"height":"100%","width":"100%","transition":".3s"});
    $("fieldset").show();
    $(".table_container").show();
    $(".nav_container").show();
    $(".nav_container").animate({width:'100%',height:'100%'},100);
  });

  $("#show_tree label").click(function(){
    o = $(this).offset();
    $('.wrapper').animate({
      scrollLeft: ($ (window). width () - $(this).width ()) / 2 + o.left,
    }, 650);
    my_input = $(this).parent().find("input").first();
    sibling_inputs = $(this).parent().parent().children($("li")).find("input").not(my_input);
    sibling_inputs.prop("checked",true);
  });
  /////////////////////// Checkbox to Radio //////////////////////
  
});
l = 0;
function activate(for_name){
  label = $('[for="'+for_name+'"]');
  l = label;
  console.log(label)
  if(label.length){
    do{
      ///////// for inputs /////////      
      label.parent().find("input").first().prop("checked",false)
      ///////// for labels /////////
      label.addClass("active");
      label = label.parent().parent().parent().find($("label")).first();
    }while(!label.hasClass("institute"))
  }
}