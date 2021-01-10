function print(abc){
	console.log(abc);
} 

function put_data(slots_json,events_json){
	for (i in slots_json){
		temp_slot = new slot(slots_json[i].pk,slots_json[i].fields.day,slots_json[i].fields.Timing_id,slots_json[i].fields.resources_filled)
		slots.push(temp_slot);
	}
	// console.table(slots);
	// events_json = JSON.parse(events_json.replace(/&#34;/ig,'"',));
	for (i in events_json){
		obj = events_json[i].fields;
		temp_event = new subject_event(events_json[i].pk,obj.Subject_id,obj.prac_carried,obj.lect_carried,obj.Faculty_id,obj.not_available
			,obj.other_events,obj.Subject_color,obj.Faculty_name)
		subject_events.push(temp_event);
	}
	console.table(subject_events);
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
	constructor(id = 0,subject_name,prac_carried,lect_carried,faculty_id,not_available
		,other_events,color,faculty_name){
		this.id = id;
		this.subject_name = subject_name;
		this.prac_carried = prac_carried;
		this.lect_carried = lect_carried;
		this.faculty_id = faculty_id;
		this.not_available = not_available;
		this.other_events = other_events;
		this.color = color;
		this.faculty_name = faculty_name
	}
}


events = [];
class event_class {
	constructor(Slot_id,Subject_event_id,Batch_id,Resource_id,Slot_id_2=null){
		this.Slot_id = Slot_id;
		this.Subject_event_id = Subject_event_id;
		this.Batch_id = Batch_id;
		this.Resource_id = Resource_id;
		this.Slot_id_2 = Slot_id_2;
	}
}


function get_slot(td){
	let day = td.index();
	let time = td.parent().attr("timing_id");
	// console.log(slots[0],day,time);
	for (i in slots){
		// print(slots[i].day);
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

function intersects(a1,a2) {
	// console.log(a1,a2);
    for (j in a1){
		if (a1[j] && a2.includes(a1[j]))
			return true
	}
	return false
}

function arraysEqual(a1,a2) {
    return JSON.stringify(a1)==JSON.stringify(a2);
}

function clear_td(td){		// refresh the td
	// console.log(td);
	if (td.length){
		td.html("");
		// td.removeAttr("filled");
	}
	return;
}

function push_event(temp_event){
	for(var i = events.length - 1;i >= 0 ;i--){
		let a1 = [events[i].Slot_id,events[i].Slot_id_2];
		let a2 = [temp_event.Slot_id,temp_event.Slot_id_2];
		if ( arraysEqual(a1,a2) && events[i].Subject_event_id == temp_event.Subject_event_id && events[i].Batch_id == temp_event.Batch_id){
			console.log("duplicate");
			return;
		}else if (intersects(a1,a2)){
			// if there is overwritting 
			b1 = events[i].Batch_id
			b2 = temp_event.Batch_id
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
					console.log("prac-lect or lect-prac");
					events.splice(i,1);
				}
			}
			clear_td(get_cell(a1[0]));
			clear_td(get_cell(a1[1]));
			// clear the old slot td
		}
	}
	events.push(temp_event);
}

function get_prac_pair(td){
	var td_below = td.closest('tr').next().children().eq(td.index());
	var td_above = td.closest('tr').prev().children().eq(td.index());
	if (td_below.length && !td_below.hasClass("isBreak")){
		return [td,td_below];
	}else if(td_above.length && !td_above.hasClass("isBreak")){
		return [td_above,td];
	}
}

function get_cell(slot_id){
	let slot_obj;
	// console.log(slot_id);
	for (i in slots){
		if (String(slots[i].id) == String(slot_id)){
			slot_obj = slots[i];
		}
	}
	if (!slot_obj)
	return false
	let tr = $("[timing_id=" + String(slot_obj.timing) + "]");
	let td = tr.find('td:nth-child('+(slot_obj.day+1)+')')
	return td;
}


function change_lect_td(td,subject_event_id,resource){	// change lecture ondrop

	let subject_event = get_subject_event(subject_event_id);
	// td.html(subject_event.subject_name);

	let card = td.children(".tt_grid");
	// .card -> button(subject_name,color)
	let card_button = card.children(".event_btn");
	card_button.html(subject_event.subject_name);
	card_button.css("background-color",subject_event.color);

	// .resource_name -> (resource_name)
	let card_resource = card.find(".resource_name");
	card_resource.html(resource);
	// .faculty_name -> (faculty_name)
	let card_faculty = card.find(".faculty_name");
	card_faculty.html(subject_event.faculty_name);
	td.addClass("filled");

}


function change_to_prac_td(td,subject_event_id) {	// change practical ondrop
	subject_event = get_subject_event(subject_event_id);
	pair = get_prac_pair(td);
	pair[0].addClass("abc");
	pair[0].html(subject_event.subject_name + " Prac");
	pair[1].html(subject_event.subject_name + " Prac");
	td.addClass("filled");
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
		// containment: $('body'),
		appendTo : "body",
		cursorAt:{top:56,left:56},
		start: function(event, ui) {
			// get all the td in which the faculty is not_available
			let subject_event = get_subject_event($(this).attr("subject_event_id"));
			// for all the not_available td add not_available
			for (i in subject_event.not_available){
				td = get_cell(subject_event.not_available[i]);
				if (!td.hasClass("filled")){
					td.addClass("not_available_td");
				}
			}
			// for all the other_events td add not_available
			for (k in subject_event.other_events){
				var obj = subject_event.other_events[k]['fields']
				event_td = get_cell(obj.Slot_id);
				if (!event_td.hasClass("filled")){
					event_td.addClass("not_available_td");
					// event_td.html(obj.Division_id)
				}
				if (obj.Slot_id_2){			// if it is practical
					event_td_2 = get_cell(obj.Slot_id_2);
					if (!event_td_2.hasClass("filled")){
						event_td_2.addClass("not_available_td");
						// event_td.html(obj.Division_id)
					}
				}
			}
			if ($(this).attr("is_prac")){
				$("td").each(function(){
					var cellIndex = $(this).index();
					var td_below = $(this).closest('tr').next().children().eq(cellIndex);
					if ($(this).hasClass("not_available_td") || td_below.hasClass("not_available_td")|| td_below.hasClass("isBreak") || !td_below.length){ 
						// || $(this).hasClass("filled") || td_below.hasClass("filled") 
						// if below is not available or filled or is break then not viable
						if (!($(this).hasClass("available_td") || $(this).hasClass("isBreak")))
							$(this).addClass("not_available_td");
					}
					else{	//	all the available
						// console.log("helr");
						$(this).addClass("available_td");
						td_below.addClass("available_td");
						td_below.removeClass("not_available_td");
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
			if (!$( this ).hasClass("not_available_td")){
			// if faculty is available at this slot
				let td = $(this);
				var slot = get_slot(td);
				$("#resources option").prop('disabled', false);
				// all the options are enabled and then the filled resources are disabled 
				$("#batches").next(".select2-container").show();
				$("#resources option[value=-1]").prop('disabled', 'disabled');
				for (i in slot.resources_filled){
					$("#resources option[value='"+String(slot.resources_filled[i])+"']").prop('disabled', 'disabled');
				}
				if (!ui.draggable.attr("is_prac")){
					$("#batches").next(".select2-container").hide();
					$("#event_form").removeAttr("is_prac");
				}
				else{
					$("#event_form").attr("is_prac",ui.draggable.attr("is_prac"));
				}
				$("#event_form").attr("slot_id",slot.id);
				$("#event_form").attr("subject_event_id",ui.draggable.attr("subject_event_id"));
				$("#event_form").show();
			}
		}
	});
	///////////////////////////// form  ///////////////////////
	$("#aform").on("click", function(){
	// $("#aform").on("click", function(){
		slot_id = $("#event_form").attr("slot_id");
		is_prac = $("#event_form").attr("is_prac");
		subject_event_id = $("#event_form").attr("subject_event_id");
		td = get_cell(slot_id);
		let batch = $("#batches").val();
		let resource = $("#resources").val();
		let resource_name = $("#resources").find(':selected').html();
		if (resource){
			if (is_prac && batch){
				temp_event = new event_class(slot_id,subject_event_id,batch,resource,String(get_slot(get_prac_pair(td)[1]).id));
				push_event(temp_event);
				change_to_prac_td(td,subject_event_id);
			}else if(!is_prac){
				temp_event = new event_class(slot_id,subject_event_id,null,resource);
				push_event(temp_event);
				change_lect_td(td,subject_event_id,resource_name);
			}else
				return;
			console.table(events);
		}else{
			return;
		}
		$("#event_form").hide();
		return;
	});
	
	$("#cancel").on("click", function(){
		$("#event_form").hide();
	});
});

function submited(){
	// console.log("JSON.stringify(events),1)");
	  $.ajax({
		  type: "post",
		  data: JSON.stringify(events),
		  success: function (){
		}
	});
}