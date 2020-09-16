$(function(){
////////////// ajax setup   /////////////////////////
    var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // Ensure jQuery AJAX calls set the CSRF header to prevent security errors
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
///////////////////////////////////////////////////////
////////////// draggable    /////////////////////////

    $(".draggable").draggable({
        revert: true,
        cursor: "move",
        cursorAt:{top:56,left:56},
        drag: function( event, ui ) {
            var select = $(this);
            event_link = select.attr("event_link");
            name = select.attr("name");
            color = select.attr("color");
            pk = select.attr("pk"); //  event_button pk
            $( this ).css("z-index","1000");	// makes the element the highest
		},
		stop: function( event, ui ) {
			$( this ).css("z-index","0");	// regularize the element
		}
    }).disableSelection();
///////////////////////////////////////////////////////
////////////// td draggable    /////////////////////////
// $(".td_div.td_div_draggable").html("s");
$(".td_div").draggable({
    revert: true,
    cursor: "move",
    cursorAt:{top:56,left:56},
    drag: function( event, ui ) {
        let child = $(this)
        let parent = child.parent();
        name =  child.html().trim();;
        color = child. css( "background-color" ); 
        pk =    parent.attr("pk");
    },
}).disableSelection();

///////////////////////////////////////////////////////
////////////// dropable    /////////////////////////

    const dropables = ".droppable";
    $( dropables ).droppable({
		// on hover
		over: function( event, ui ) {
			let td = $( this );
			td.css({"background-color":"#7377a5"})			
			td.parent().find('th').css({"background-color":"#7377a5"});
			// the th of timing is selected
			tdIndex = td.index() + 1;
			$('.main_table tr').find('th:nth-child(' + tdIndex + ')').css({"background-color":"#7377a5"});
			// th of day is selected
		},
		// on out
		out: function( event, ui ) {
			let td = $( this );
			td.css({"background-color":""})
			td.parent().find('th').css({"background-color":""});
			// the th of timing is selected
			let tdIndex = td.index() + 1;
			$('.main_table tr').find('th:nth-child(' + tdIndex + ')').css({"background-color":""});
			// th of day is selected
		},

        drop: function( event, ui ) {
			let td = $( this );
			let div = td.find("div");   // get child div of td
			td.attr({"pk":pk}); //set attirbute of parent
			div.html(name)
			div.css({"background-color":color})
			td.css({"background-color":""})
			td.parent().find('th').css({"background-color":""});
			// the th of timing is selected
			let tdIndex = td.index() + 1;
			$('.main_table tr').find('th:nth-child(' + tdIndex + ')').css({"background-color":""});
			// th of day is selected
			// obj.click(function(){open(event_link);});
			// making cells clickable
		}
		
    });
    $('#trash').droppable({
        drop: function(event, ui) {
            let dropped_obj = ui.draggable[0];
            let class_of_obj = dropped_obj.getAttribute("class").split(' ')[0];
            if (class_of_obj == "td_div"){
				let parent = dropped_obj.parentElement;
				console.log("j-");
                parent.removeAttribute("pk");
                dropped_obj.removeAttribute("style");
                dropped_obj.innerHTML = "";
            }
        }
    });
});

function openform(){
    document.getElementById('form-container-id').style.display = "flex";
}

function closeform(){
    document.getElementById('form-container-id').style.display = "none";
}

///////////////////////////////////////////////////////
////////////// save click     /////////////////////////
document.getElementsByClassName('save')[0].onclick = function(){
  swal({
    title: "Warning!",
    text: "Your previous data will be overwritten.",
    icon: "warning",
    buttons: ["Cancel","Save"],
  })
  .then((willDelete) => {
  if (willDelete) {
    swal("", {
      icon: "success",
      text : "Saved"
    });

    let text;
    var table = $('.main_table').tableToJSON(// calling tableToJSON
    {
      extractor : function(cellIndex, $cell) {
          if(cellIndex == '0' ){// if it is t-heading
              text = $cell.find('p').html().trim();
              p = $cell.attr('pk');// get attribute period primary key
              return {
                // name: $cell.find('span').text(),
                time:text,
                time_pk:p,
              };
          }
          else{
              return {
                  name: $cell.text().trim(),
                  event_pk: $cell.attr('pk'),// set attribute period primary key
                  time_pk: p,
                  day: $cell.attr('day'),// set attribute day
              };
          }
      }
    }); // Convert the table into a javascript object
    let state = JSON.stringify(table); // final JSON to be passed through ajax
    console.log(state);
    // alert(state);
    $.ajax({
        type: "post",
        data: state,
        url: ""
    });

  }
  else {
    swal("Your changes are not saved!");
  }
});
}
