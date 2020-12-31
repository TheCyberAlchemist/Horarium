function put_data(slots_json,events_json){
	json = JSON.parse(slots_json.replace(/&#34;/ig,'"',));
	for (i in json){
		temp_slot = new slot(json[i].pk,json[i].fields.day,json[i].fields.Timing_id)
		slots.push(temp_slot);
	}
	events_json = JSON.parse(events_json.replace(/&#34;/ig,'"',));
	// console.log(events_json);
	for (i in events_json){
		obj = events_json[i].fields;
		temp_event = new subject_event(events_json[i].pk,obj.Subject_id,obj.prac_carried,obj.lect_carried,obj.Faculty_id,obj.not_available,obj.other_events)
		subject_events.push(temp_event);
	}
	console.table(subject_events);
}

var slots = [];
class slot{
	constructor(id = 0,day = 0,timing = 0){
		this.id = id;
		this.day = day;
		this.timing = timing;
	}
}

subject_events = [];
class subject_event {
	constructor(id = 0,subject_name,prac_carried,lect_carried,faculty_id,not_available,other_events){
		this.id = id;
		this.subject_name = subject_name;
		this.prac_carried = prac_carried;
		this.lect_carried = lect_carried;
		this.faculty_id = faculty_id;
		this.not_available = not_available;
		this.other_events = other_events;		
	}
}


events = [];
class event_class {
	constructor(slot,subject_event,resource){
		this.slot = slot;
		this.subject_event = subject_event;
		this.resource = resource;

	}
}


function get_slot(td){
	let day = td[0].cellIndex;
	let time = td.parent().attr("timing_id");
	console.log(slots[0],day,time);
	for (i in slots){	
		if (slots[i].day == day && slots[i].timing == time){
			return slots[i].id;
		}
	}
}

function get_cell(slot_id){
	let slot_obj;
	for (i in slots){
		if (slots[i].id == slot_id){
			slot_obj = slots[i];
		}
	}
	let tr = $("[timing_id=" + String(slot_obj.timing) + "]");
	let td = tr.find('td:nth-child('+(slot_obj.day+1)+')')
	// console.log(td);
	return td;
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
	$(".draggable").draggable({
		revert: true,
		cursor: "move",
		helper: "clone",
		cursorAt:{top:56,left:56},
		start: function(event, ui) {
			subject_event_id = $(this).attr("subject_event_id");
			// get all the td in which the faculty is not_available
			for (j in subject_events){
				if (subject_events[j].id == subject_event_id){
					// for all the not_available td
					for (i in subject_events[j].not_available){
						td = get_cell(subject_events[j].not_available[i]);
						if (!td.hasClass("filled")){
							td.addClass("not_available_td");
						}
					}
					// for all the other_events td
					for (k in subject_events[j].other_events){
						var obj = subject_events[j].other_events[k]['fields']
						event_td = get_cell(obj.Slot_id);
						if (!event_td.hasClass("filled")){
							event_td.addClass("not_available_td");
							event_td.html(obj.Division_id)
						}
					}
				}
			}
			if ($(this).attr("is_prac")){
				$("td").each(function(){
					var cellIndex = $(this).index();
					var td_below = $(this).closest('tr').next().children().eq(cellIndex);
					if (td_below.hasClass("not_available_td") || td_below.hasClass("filled") || td_below.hasClass("isBreak") || !td_below.length){
						// if below is not available or filled or is break then not viable
						$(this).addClass("not_available_td");
					}
					else if (!td.hasClass("not_available_td")){	//	all the available
						$(this).addClass("available_td");
						// $(this).addClass("available_td");
						// td_below.removeClass("not_available_td");
						// td_below.addClass("available_td");
					}
				});
			}
		 },
		drag: function( event, ui ) {
		},
		stop: function( event, ui ) {
			$("td").each(function(){
				$(this).removeClass("not_available_td");
				$(this).removeClass("available_td");

			});
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
			if (!td.hasClass("not_available_td")){ // if faculty is available at this slot
				let div = td.find("div");   // get child div of td
				temp_event = new event_class(get_slot($(this)),subject_event_id);
				events.push(temp_event);
				console.table(temp_event);
				td.addClass("filled");
				td.css({"background-color":"red"})
			}
		}
	});
});