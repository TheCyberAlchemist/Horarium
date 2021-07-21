$(document).ready(function(){
  activate();
  /////////////////////// Navbar Animation //////////////////////
  $(".navtree_wrapper").animate({height:"0%",},0);
  // offset = 0
  // console.log(offset);
  $(".navtree_wrapper").show();
  offset = l.length? l.offset() : 0;
  $(".navtree_wrapper")[0].scrollTo(offset.left+(screen.width/1.5),offset.top);
  $(".me").click(function(){
    // $("#whole_container_id").css({"height":"0%","width":"0%","transition":".3s"});
    $(".main_content").css({"height":"0%","width":"0%","transition":".3s"});
      // $('.navtree_wrapper').animate({
      //       scrollTop: offset.top,
      //       scrollLeft: offset.left/1.5,
      //   }, 0);
    $(".navtree_wrapper").animate({height:'100%'},300);
    $(".navtree_wrapper").animate({height:'95%'},250);
    $(".navtree_wrapper").animate({height:'100%'},200);
    $(".navtree_wrapper").animate({height:'98%'},100);
    $(".navtree_wrapper").animate({height:'100%'},100);
    $(".navtree_wrapper").animate({height:'99%'},80);
    $(".navtree_wrapper").animate({height:'100%'},70);
    //$(".toggle_button").css({"height":"40px","width":"50px"});
    $(".toggle_button").animate({height:'40px',width:'50px'},10);
    $("fieldset").hide();
    $(".table_container").hide();
    $(".nav_container").hide();
    if($(".table_and_card")) {
      console.log("table&card hide");
      $(".table_and_card").hide();
    }
      //$(".nav_container").animate({width:'0%',height:'0%'},100);
  });
  
  $(".not_me").click(function(){
    $(".toggle_button").css({"height":"0px","width":"0px"});
    $(".navtree_wrapper").animate({height:'0%'},400);
    $(".main_content").css({"height":"100%","width":"100%","transition":".3s"});
    $("fieldset").show();
    $(".table_container").show();
    $(".nav_container").show();
    $(".nav_container").animate({width:'100%',height:'100%'},100);
    $("#add_slot_form").hide();
    if($(".table_and_card")) {
      console.log("table&card show");
      $(".table_and_card").show();
    }
  });

  $("#show_tree .data").click(function(){
      my_input = $(this).parent().find("input").first();
      sibling_inputs = $(this).parent().parent().children($("li")).find("input").not(my_input);
      sibling_inputs.prop("checked",true);
      setTimeout(function(){
        o = my_input.parent().offset();
        $('.navtree_wrapper')[0].scrollTo({
          top:o.top,
          left:o.left+my_input.parent().width()+(screen.width/1.5),
          behavior: 'smooth'
        });
      }, 250);
  });
  /////////////////////// Checkbox to Radio //////////////////////
  
});
l = 0;
function activate(){
  for_name = $("#page_activator").attr("activate-page");
  label = $('[for="'+for_name+'"]');
  if (for_name =="home"){
    label.addClass("active");
    return
  }
  if(label.length){
    do{
      ///////// for inputs /////////      
      label.parent().find("input").first().prop("checked",false)
      ///////// for labels /////////
      label.addClass("active");
      label = label.parent().parent().parent().find($("label")).first();
    }while(!label.hasClass("institute"))
  }
  l = label;
  // we can also keep it such that the parent is center
  // console.log(label);
}