function put_data(slots_json){
	json = JSON.parse(slots_json.replace(/&#34;/ig,'"',));
	for (i in json){
		temp_slot = new slot(json[i].pk,json[i].fields.day,json[i].fields.Timing_id)
		slots.push(temp_slot);
		// console.log(json[i].fields.Timing_id);
	}
}
var slots = []
class slot{
	constructor(id = 0,day = 0,timing = 0){
		this.id = id;
		this.day = day;
		this.timing = timing;
	}
}
function get_slot(time,day){
	for (i in slots){
		if (slots[i].day == day && slots[i].timing == time){
			return slots[i].id;
		}
	}
}
events = []
class event_class {
	constructor(slot = 0,subject_event = 0){
		this.slot = slot;
		this.subject_event = subject_event;
	}
}

$(document).ready (function () {
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
	$(".draggable").draggable({
		revert: true,
		cursor: "move",
		helper: "clone",
		cursorAt:{top:56,left:56},
		drag: function( event, ui ) {
			subject_event_id = $(this).attr("subject_event_id");
		},
		stop: function( event, ui ) {
		}

	}).disableSelection();

	$( ".droppable" ).droppable({
		// on hover
		over: function( event, ui ) {
		},
		// on out
		out: function( event, ui ) {
		},
		drop: function( event, ui ) {
			let td = $( this );
			let div = td.find("div");   // get child div of td
			let day = $(this)[0].cellIndex;
			let time = $(this).attr("timing_id");
			temp_event = new event_class(get_slot(time,day),subject_event_id);
			events.push(temp_event);
			// console.log(temp_event);
			td.css({"background-color":"red"})
		}
	});
});
function submited(){
	console.log(JSON.stringify(events),1);
	  $.ajax({
		  type: "post",
		  data: JSON.stringify(events),
		  success: function (){
		  }
	  });
  }