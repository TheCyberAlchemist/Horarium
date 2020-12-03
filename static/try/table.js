function put_data(slots_json){
	json = JSON.parse(slots_json.replace(/&#34;/ig,'"',));
	for (i in json){
		temp_slot = new slot(json[i].pk,json[i].fields.day,json[i].fields.Timing_id)
		slots.push(temp_slot);
		// console.log(json[i].fields.Timing_id);
	}
	// console.log(slots);

}
var events_json;
var not_available_json;
function put_events(events,not_available){
	events_json = JSON.parse(events.replace(/&#34;/ig,'"',));
	not_available_json = JSON.parse(not_available.replace(/&#34;/ig,'"',));
	console.log(events_json,not_available_json)
}
var slots = [];
class slot{
	constructor(id = 0,day = 0,timing = 0){
		this.id = id;
		this.day = day;
		this.timing = timing;
	}
}

function get_slot(td){
	let day = td[0].cellIndex;
	let time = td.parent().attr("timing_id");
	// console.log(day,time)
	for (i in slots){
		if (slots[i].day == day && slots[i].timing == time){
			return slots[i].id;
		}
	}
}



events = [];
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
	///////////////////////////// Time Table ///////////////////////
	if($(".draggable").length){	// if draggable is present
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
			
			temp_event = new event_class(get_slot($(this)),subject_event_id);
			events.push(temp_event);
			// console.log(temp_event);
			td.css({"background-color":"red"})
		}
	});
	}
	///////////////////////////// Not Asvailable ///////////////////////
	else if($(".submit_not_avail").length){
		for(i in events_json){		// all the events are marked and disabled
			var td = get_cell(events_json[i])
			td.find("input[type='checkbox']").removeAttr("name");
			td.css({"backgroundColor" : "blue","opacity" : ".5"})
		}
		for(i in not_available_json){	// all the not_available are checked
			get_cell(not_available_json[i]).find("input[type='checkbox']").prop("checked", true);
		}
		function change_css(){			// changes the color of all when called
			$("tbody").find("input:checkbox[name=not_available]").each(function(){
				checkbox = $(this);
				td = $(this).parent();
				if(checkbox.prop("checked") == true){ // if checked 
					td.css({"backgroundColor" : "red","opacity" : ".5"});
				}
				else if(checkbox.prop("checked") == false){	// not checked 
					td.css({"backgroundColor" : "transparent","opacity" : "1"});
				}
			});
		}
		change_css();
		function get_cell(obj){
			// [id=choose]
			let tr = $("[timing_id=" + String(obj['fields'].Timing_id) + "]");
			let td = tr.find('td:nth-child('+(obj['fields'].day+1)+')')
			console.log(td);
			return td;
		}
		$(".td").click(function(){
			var checkbox = $(this).find("input[type='checkbox']");
			checkbox.prop("checked", !checkbox.prop("checked"));
			change_css();
		});

		$(".day").click(function(){
			var index = $(this)[0].cellIndex;
			var td = $('tbody').find('td:nth-child('+(index+1)+')');
			var input = td.find("input[type='checkbox']");
			var checkbox = $(this).find("input[type='checkbox']");	// day checkbox
			checkbox.prop("checked", !checkbox.prop("checked"));
			var value = checkbox.prop("checked")
			input.each(function(i,obj){
				$(this).prop("checked",value);
			});
			change_css()
		});
		
		$(".time").click(function(){
			var tr = $(this).parent();
			var td = tr.find('td');
			var input = td.find("input[type='checkbox']");
			var checkbox = $(this).find("input[type='checkbox']");
			checkbox.prop("checked", !checkbox.prop("checked"));
			var value = checkbox.prop("checked")
			input.each(function(i,obj){
				$(this).prop("checked",value);
			});
			td.each(function(i,obj){
			});
			change_css();
		});

		$(".submit_not_avail").click(function(){
			var checked = [];
			$("tbody").find("input:checkbox[name=not_available]:checked").each(function(){
				parent_td = $(this).parent()
				checked.push(get_slot(parent_td));
			});
			$.ajax({
				type: "post",
				data: JSON.stringify(checked),
				success: function (){
				}
			});
			// console.log(checked);
		});
		}
});
function submited(){
	// console.log(JSON.stringify(events),1);
	  $.ajax({
		  type: "post",
		  data: JSON.stringify(events),
		  success: function (){
		  }
	  });
  }