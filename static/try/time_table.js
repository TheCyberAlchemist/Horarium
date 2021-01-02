function print(abc){
	console.log(abc);
}
function put_data(slots_json,events_json){
	json = JSON.parse(slots_json.replace(/&#34;/ig,'"',));
	for (i in json){
		temp_slot = new slot(json[i].pk,json[i].fields.day,json[i].fields.Timing_id,json[i].fields.resources_filled)
		slots.push(temp_slot);
	}
	// console.table(slots);
	events_json = JSON.parse(events_json.replace(/&#34;/ig,'"',));
	for (i in events_json){
		obj = events_json[i].fields;
		temp_event = new subject_event(events_json[i].pk,obj.Subject_id,obj.prac_carried,obj.lect_carried,obj.Faculty_id,obj.not_available,obj.other_events)
		subject_events.push(temp_event);
	}
	// console.table(subject_events);
}

var slots = [];
class slot{
	constructor(id = 0,day = 0,timing = 0,resources_filled=0){
		this.id = id;
		this.day = day;
		this.timing = timing;
		this.resources_filled = resources_filled;
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
	constructor(slot,subject_event,batch,resource){
		this.slot = slot;
		this.subject_event = subject_event;
		this.batch = batch;
		this.resource = resource;

	}
}


function get_slot(td){
	let day = td[0].cellIndex;
	let time = td.parent().attr("timing_id");
	// console.log(slots[0],day,time);
	for (i in slots){	
		if (slots[i].day == day && slots[i].timing == time){
			return slots[i];
		}
	}
}

function get_subject_event(id){
	// console.log(slots[0],day,time);
	for (j in subject_events){
		if (subject_events[j].id == id){
			return subject_events[j]
		}
	}
}

function push_event(temp_event){
	for(i in events){
		if (events[i].slot == temp_event.slot && events[i].subject_event == temp_event.subject_event){
			console.log("duplicate");
			return;
		}else if (events[i].slot == temp_event.slot){
			// if there is en event on the slot
			b1 = events[i].batch
			b2 = temp_event.batch
			if (b1 == b2){
				// if lect-lect or prac(b1)-prac(b1)
				console.log("lect-lect or prac(b1)-prac(b1)");
				events.splice(i,1);
			}else{
				if (b1 && b2){
					// if both not null prac(b1)-prac(b2)
					console.log("prac(b1)-prac(b2)");
				}else{
					// if lect-prac or prac-lect
					console.log("lect-prac or prac-lect");
					events.splice(i,1);
				}
			}
		}
	}
	events.push(temp_event);
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

function change_td(td){
	// td.css({"background-color":"white"});
	subject_event = get_subject_event(subject_event_id);

	card = td.children(".card");
	// .card -> span (batch)
	card_span = card.children("span");
	// .card -> button(subject_name,color)
	card_span = card.children("button");
	// .resource_name -> (resource_name)

	// .faculty_name -> (faculty_name)

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
			// get all the td in which the faculty is not_available
			let subject_event = get_subject_event($(this).attr("subject_event_id"));
				// for all the not_available td
				for (i in subject_event.not_available){
					td = get_cell(subject_event.not_available[i]);
					if (!td.hasClass("filled")){
						td.addClass("not_available_td");
					}
				}
				// for all the other_events td
				for (k in subject_event.other_events){
					var obj = subject_event.other_events[k]['fields']
					event_td = get_cell(obj.Slot_id);
					if (!event_td.hasClass("filled")){
						event_td.addClass("not_available_td");
						// event_td.html(obj.Division_id)
					}
				}
			if ($(this).attr("is_prac")){
				$("td").each(function(){
					var cellIndex = $(this).index();
					var td_below = $(this).closest('tr').next().children().eq(cellIndex);
					// console.log(td_below.hasClass("not_available_td"));
					if ($(this).hasClass("not_available_td") || td_below.hasClass("not_available_td") || td_below.hasClass("filled") || td_below.hasClass("isBreak") || !td_below.length){
						// if below is not available or filled or is break then not viable
						if (!($(this).hasClass("available_td") || $(this).hasClass("isBreak")))
							$(this).addClass("not_available_td");
					}
					else{	//	all the available
						// console.log("helr");
						$(this).addClass("available_td");
							td_below.removeClass("not_available_td");
							td_below.addClass("available_td");
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
		// on drop 
		drop: function( event, ui ) {
			if (!$( this ).hasClass("not_available_td")){ // if faculty is available at this slot
				let td = $(this);
				var slot = get_slot(td);
				// print(slot);
				// all the options are enabled and then the filled resources are disabled 
				$("#batches").next(".select2-container").show();
				for (i in slot.resources_filled){
					$("#resources option[value='"+String(slot.resources_filled[i])+"']").prop('disabled', 'disabled');
				}
				if (!ui.draggable.attr("is_prac")){
					$("#batches").next(".select2-container").hide();
				}
				$("#event_form").attr("slot_id",slot.id);
				$("#event_form").attr("is_prac",ui.draggable.attr("is_prac"));
				$("#event_form").attr("subject_event_id",ui.draggable.attr("subject_event_id"));
				$("#event_form").show();
			}
		}
	});
	$("#aform").on("click", function(){
	// $("#aform").on("click", function(){
		slot_id = $("#event_form").attr("slot_id");
		is_prac = $("#event_form").attr("is_prac");
		subject_event_id = $("#event_form").attr("subject_event_id");
		td = get_cell(slot_id);
		let batch = $("#batches").val();
		let resource = $("#resources").val();
		// print([batch,resource,slot.id]);
		if (resource){
			if (is_prac && batch)
				temp_event = new event_class(slot_id,subject_event_id,batch,resource);
			else if(!is_prac)
				temp_event = new event_class(slot_id,subject_event_id,null,resource);
			else
				return;
			push_event(temp_event);
			console.table(events);
			td.addClass("filled");
			change_td(td);
		}
		$("#event_form").hide();
		return;
	});
	$("#cancel").one("click", function(){
		$("#event_form").hide();
	});
	// lect1 = new event_class(2,7,null,1);
	// lect2 = new event_class(2,3,null,1);
	// prac1b1 = new event_class(2,7,1,1);
	// prac2b1 = new event_class(2,3,1,1);
	// prac2b2 = new event_class(2,7,2,1);
	// // console.log(prac1b1.batch);
	// push_event(lect1);
	// push_event(new event_class(4,7,1,1));
	// push_event(prac1b1);
	// // push_event(new event_class(4,7,1,1));
	// console.table(events);
});