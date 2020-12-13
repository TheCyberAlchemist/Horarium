$(document).ready(function () {
  ////////////// ajax setup   /////////////////////////
  var csrftoken = Cookies.get('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  // Ensure jQuery AJAX calls set the CSRF header to prevent security errors
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  /*//////////////DROPDOWN//////////////*/
  if ($("#designations").length) {
    $("#designations").select2();
    $("#shifts").select2();
  }
  if ($("#day1").length) {
    $("#day1").select2();
    $("#day2").select2();
  }
  if ($("#batches").length) {
    $("#batches").select2();
  }
  if ($("#slot_naming").length) {
    $("#slot_naming").select2();
  }
  /* ///////////TO UpperCase/////////////// */

  // $('.short_names').val($('.short_names').val().toUpperCase());

  $(".submit_button").click(function () {
    if ($('.short_names').length)
      $('.short_names').val($('.short_names').val().toUpperCase());
  });
  // /* //////Scroll into view ///////// */


  /**//////////// Can Teach ///////////////////
  $('.can_container li :checkbox').on('click', function () {
    var $chk = $(this);
    var $li = $chk.closest('li');
    var $ul, $parent;
    if ($li.has('ul')) {
      $li.find(':checkbox').not(this).prop('checked', this.checked);
    }
    do {
      $ul = $li.parent();
      $parent = $ul.siblings(':checkbox');
      if ($chk.is(':checked')) {
        $parent.prop('checked', $ul.has(':checkbox:not(:checked)').length == 0)
      } else {
        $parent.prop('checked', false)
      }
      $chk = $parent;
      $li = $chk.closest('li');
    } while ($ul.is(':not(.someclass)'));
  });

  /** //////////Subject Color Palette //////////////////*/
  $(".colors").click(function () {
    if ($(".colors").css({ "border": "none" })) {
      $(this).css({ "border": "5px solid black" });
    }
    // else {
    //   $(this).css({"border":"none","borderRadius" :"7px","opacity":"1" });
    // }
  });

  valid_input();
  $(".form_input").change(function () {
    valid_input();
  })
  $(".form_input").focus(function () {
    $(this).next(".form_input_label").find(".text").css({
      "top": "-.7em",
      "left": ".5px",
      "transition": ".2s",
      "font-size": "16px",
      "color": "rgb(185, 184, 184)"
    });
  });

  $(".form_input").blur(function () {
    if ($(this).prop("type") != "time") {
      if (!$(this).val()) {
        $(this).next().find(".text").css({
          "position": "absolute",
          "top": " 1.2em",
          "left": "2em",
          "color": "white",
          "pointer-events": "none",
          "user-select": "none",
          "font-size": "18px",
          "transition": ".4s",
        });
      }
    }
  });

  if ($("#first_form").length) {  //if there is firstform
    $("#first_form").css({ // to make slotDetails Pop Up in center
      "position": "absolute",
      "top": "50%",
      "left": "50%",
      "transform": "translate(-50%,-50%)",
      "opacity": "1",
      "z-index": "100",
    });
    $("#whole_container_id,.submit_button_container").addClass("blur_background");
    //check #first_form_submit in slot.js  
  }
  $(".form_hider").click(function () {
    $(".myform").hide();
    $(".form_visibility_img_container").show();
    $(".pagination_container").hide();
  });
});
function valid_input() {
  var inputs = $(".form_input");
  inputs.each(function (i, obj) {
    if ($(this).val()) {
      $(this).next().find(".text").css({
        "top": "-.7em",
        "left": ".5px",
        "transition": ".2s",
        "font-size": "16px",
        "color": "rgb(185, 184, 184)"
      });
    }
  });
  var update_div = $(".update_div");
  update_div.next().find(".text").css({
    "top": "-.7em",
    "left": ".5px",
    "transition": ".2s",
    "font-size": "16px",
    "color": "rgb(185, 184, 184)"
  });
}
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
  else if (a.type === "text") {
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
  else if (x.type === "text") {
    x.type = "password";
    y.style.display = "none";
    z.style.display = "inline";
  }
}

function delete_entries() {
  var checked = $('input[name="del"]:checked').map(function () { return this.value; }).get()
  let state = JSON.stringify(checked);
  if (checked.length) {  // checkes if one or more are selected or not
    // console.log(state)
    $.ajax({
      type: "post",
      data: state,
      success: function () {
        location.reload(); // reload page after success of post
      }
    });
  }
}


function form_visibility() {

  var form = document.getElementsByClassName("myform")[0];
  var p = document.getElementById("myp");
  var pages = document.getElementsByClassName("pagination_container")[0];
  var container = document.getElementsByClassName("form_visibility_img_container")[0];
  if (form.style.display == "none") {
    // p.innerHTML = "Close Form";
    container.style.display = "none";
    form.style.display = "block";
    if (pages)
      pages.style.display = "";
  }
  else {
    p.innerHTML = "Show Form";
    form.style.display = "none";
    if (pages)
      pages.style.display = "none";
  }
}

function show_error(json_error) {
  // console.log(json_error);
  json = JSON.parse(json_error.replace(/&#34;/ig, '"',));
  for (i in json) {
    var input = $("[name=" + i + "]");
    console.log(input);
    // change css here 
    $('.myform .input_container :input').val('');
  }

  form_visibility();
  for (i in json) {
    input = $("[name=" + i + "]");
    break
  }
  input.focus()
  // input[0].setCustomValidity('hii');
}
