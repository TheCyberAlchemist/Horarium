function print(abc){
	console.log(abc);
	return true;
}


function get_prac_pair(td){
	var td_below = td.closest('.my_row').next().children().eq(td.index());
	var td_above = td.closest('.my_row').prev().children().eq(td.index());
	if (td_below.length && !td_below.hasClass("isBreak")){
		return [td,td_below];
	}else if(td_above.length && !td_above.hasClass("isBreak")){
		return [td_above,td];
	}
}


var batches = [];
var subjects = [];
function put_data(slots_json,sub_events_json,batches,old_events_json,subjects_json){
	for (i in slots_json){
		temp_slot = new slot(slots_json[i].pk,slots_json[i].fields.day,slots_json[i].fields.Timing_id,slots_json[i].fields.resources_filled)
		slots.push(temp_slot);
	}
	// console.table(slots);
	// events_json = JSON.parse(events_json.replace(/&#34;/ig,'"',));
	for (i in sub_events_json){
		obj = sub_events_json[i].fields;
		temp_sub_event = new subject_event(sub_events_json[i].pk,obj.Subject_name,obj.Subject_id,obj.prac_carried,obj.lect_carried,obj.Faculty_id,obj.not_available
			,obj.other_events,obj.Subject_color,obj.Faculty_name)
		subject_events.push(temp_sub_event);
	}
	this.batches=batches;
	this.subjects = subjects_json;
	// console.table(old_events_json);
	for(i in old_events_json){
		obj = old_events_json[i];
		temp_event = new event_class(obj.Slot_id,obj.Subject_event_id,obj.Batch_id,obj.Resource_id,obj.Slot_id_2);
		td = get_cell(obj.Slot_id);
		let resource = "";
		$("#resources option").each(function(){
			if ($(this).val() == obj.Resource_id){
				resource = $(this).html();
			}
		});
		if (temp_event.Slot_id_2){	// if it is a practical		
			// print(temp_event);
			if (push_event(temp_event)){
				// console.log(td);
				if (!td.html()){
					change_to_prac_td(td,get_batches(obj.Subject_event_id,true));
				}
				put_prac(td,obj.Subject_event_id,obj.Batch_id,resource);
			}
		}else{	
			if (push_event(temp_event)){
				if (!td.html()){
					change_to_lect_td(td,get_batches(obj.Subject_event_id,false));
				}
				put_lect(td,obj.Subject_event_id,resource,obj.Batch_id);
			}
		}
	}

	// console.table(events);
	// console.table(subjects);
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
	constructor(id = 0,subject_name,subject_id,prac_carried,lect_carried,faculty_id,not_available
		,other_events,color,faculty_name){
		this.id = id;
		this.subject_name = subject_name;
		this.subject_id = subject_id;
		this.prac_carried = prac_carried;
		this.lect_carried = lect_carried;
		this.faculty_id = faculty_id;
		this.not_available = not_available;
		this.other_events = other_events;
		this.color = color;
		this.faculty_name = faculty_name;
	}
}


events = [];
class event_class {
	constructor(Slot_id,Subject_event_id,Batch_id,Resource_id,Slot_id_2=null){
		this.Slot_id = Slot_id;
		this.Subject_event_id = Subject_event_id;
		this.Batch_id = Batch_id?Batch_id:null;
		this.Resource_id = Resource_id?Resource_id:null;
		this.Slot_id_2 = Slot_id_2?Slot_id_2:null;
	}
	toString() {
        return `(${get_cell(this.Slot_id)}, ${get_subject_event(this.Subject_event_id).subject_name})`
    }
}


function push_event(temp_event){
	// check for batches in event_counter too

	let a2 = [temp_event.Slot_id,temp_event.Slot_id_2];
	let subject_event = get_subject_event(temp_event.Subject_event_id);
	let is_prac = Boolean(a2[1]);

	// if (is_prac && event_counter(temp_event) >= subject_event.prac_carried){
	// 	console.log("max_filled");
	// 	return false;
	// }else if (!is_prac && event_counter(temp_event) >= subject_event.lect_carried){
	// 	console.log("max_filled");
	// 	return false;
	// } 
	if (!subject_event_has_load_remaining(temp_event.Subject_event_id,is_prac) || !subject_has_load_for_batch(subject_event.subject_id,temp_event.Batch_id,is_prac)){
		console.log("max_filled");
		return false;
	}
	for(var i = events.length - 1;i >= 0 ;i--){
		let a1 = [events[i].Slot_id,events[i].Slot_id_2];
		if ( arraysEqual(a1,a2) && events[i].Subject_event_id == temp_event.Subject_event_id){
			console.log("duplicate");
			return false;
		}else if (intersects(a1,a2)){
			// if there is overwritting 
			b1 = events[i].Batch_id
			b2 = temp_event.Batch_id
			if (b1 == b2){
				// if lect-lect or prac(b1)-prac(b1)
				console.log("lect-lect or prac(b1)-prac(b1)");
				events.splice(i,1);
				clear_td(get_cell(a1[0]));
				clear_td(get_cell(a1[1]));
			}else{
				if (b1 && b2){
					// if both not null prac(b1)-prac(b2)
					console.log("prac(b1)-prac(b2)");
				}else{
					// if lect-prac or prac-lect
					console.log("prac-lect or lect-prac");
					events.splice(i,1);
					clear_td(get_cell(a1[0]));
					clear_td(get_cell(a1[1]));
				}
			}
			
			// clear the old slot td
		}
	}
	events.push(temp_event);
	update_card(subject_event,is_prac);
	// if (!subject_event_has_load_remaining(temp_event.Subject_event_id,is_prac)){
	// 	// get the card and disable it
	// }

	// if (is_prac && event_counter(temp_event) >= subject_event.prac_carried){
	// 	// get card and disable it
	// }else if (!is_prac && event_counter(temp_event) >= subject_event.lect_carried){
	// 	// get card and disable it	
	// }
	return true;
}

function update_card(subject_event,is_prac) {
	let event_arr = events.filter(e => e.Subject_event_id==subject_event.id && Boolean(e.Slot_id_2) == is_prac);
	let remaining;
	if (is_prac){
		remaining = subject_event.prac_carried - event_arr.length;
		$(`[subject_event_id = ${subject_event.id}][is_prac = ${is_prac}]`);
	}else{
		remaining = subject_event.lect_carried - event_arr.length;
		$(`[subject_event_id = ${subject_event.id}]`);
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


function subject_event_has_load_remaining(subject_event_id,is_prac=false){
	let subject_event = get_subject_event(subject_event_id);
	let event_arr = events.filter(e => e.Subject_event_id==subject_event_id && Boolean(e.Slot_id_2) == is_prac);
	total_similar_events = event_arr.length;
	if (total_similar_events){
		// event_arr
		if (event_arr[0].Slot_id_2){	// if it was a practical
			if (subject_event.prac_carried > total_similar_events){
				return true;
			}
		}else{							// if it was a lecture
			if (subject_event.lect_carried > total_similar_events){
				return true;
			}
		}
	}else if (!total_similar_events){ // if no event is still there
		return true;
	}
	console.log(`max filled - ${subject_event.subject_name}`,is_prac);
	return false;
}



function subject_has_load_for_batch(subject_id,batch_id,is_prac) {
	let subject = subjects.filter(e=> e.pk == subject_id)[0].fields;
	// console.log(subject_id);
	if (is_prac && subject.prac_per_week){
		let all_events_for_subject_in_same_batch = events.filter(e=> e.Slot_id_2 && e.Batch_id==batch_id && get_subject_event(e.Subject_event_id).subject_id == subject_id);
		if (subject.prac_per_week > all_events_for_subject_in_same_batch.length ){
			return true;
		}
	}else if (!is_prac && subject.lect_per_week){
		let all_events_for_subject_in_same_batch = events.filter(e=> !e.Slot_id_2 && e.Batch_id==batch_id && get_subject_event(e.Subject_event_id).subject_id == subject_id);
		if (subject.lect_per_week > all_events_for_subject_in_same_batch.length ){
			return true;
		}
	}
	console.log(`max filled for batch ${batch_id} - ${subject.name}`,is_prac);
	return false;
}


function get_batches(subject_event_id,is_prac=false){	// get all the batches that consist the subject event(P/L)
	let subject_id = get_subject_event(subject_event_id).subject_id;
	let temp = [];
	for (i in batches){
		let batch = batches[i].fields;
		if((is_prac && batch.batch_for == "prac") || (!is_prac && batch.batch_for == "lect")){
			// if the related subject prac or lect has the batch
			if (batch.subjects_for_batch.includes(subject_id))
				temp.push(batches[i]);
		}
	}
	if (temp.length){
		return temp;
	}
	return false;
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
		if(td.hasClass("prac")){
			td.removeClass("prac");
			td.removeClass("prac_above");
			td.removeClass("prac_below");
			td.removeClass("prac_below");
		}
		td.removeClass("filled");
		td.addClass("lect");
	}
	return;
}


function get_event_index_by_slot(slot){
	for(i in events){
		if(events[i].Slot_id == slot || events[i].Slot_id_2 == slot){
			return i;
		}
	}
	return false;
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
		return $("#kaibhi");
	let tr = $("[timing_id=" + String(slot_obj.timing) + "]");
	let td = tr.find('.my_col:nth-child('+(slot_obj.day+1)+')')
	// print(tr);
	return td;
}

function change_to_lect_td(td,subject_batch){
	let colspan;
	let string = "";
	// console.log(subject_batch);
	has_batch = Boolean(subject_batch);
	// console.log(has_batch);
	if (has_batch){		// if lect_batch
		colspan = (12/subject_batch.length);
		string +=  `<div class="row my-auto text-center" >`;
		for (let i in subject_batch){
			string +=
			 `<div class="col-`+colspan+`" batch_for=`+subject_batch[i].pk+` data-toggle="tooltip" data-placement="bottom" title="" >
				<button class="event_name lect_mycol mt-2 lect_batches"></button>
			</div>`;
		}
		string += `</div>`;
	}else{
		string +=
		`<div class='row p-2'>
			<div class='col-12'>
				<button class='event_name btn mt-1 mb-1' style = 'color:white;'></button>
			</div>
			<div class='col-6 text-left' class = "faculty_name"></div>
			<div class='col-6 text-right' class = "resource_name"></div>
		</div>`
	}
	td.html(string);
	td.addClass("filled");
}


function put_lect(td,subject_event_id,resource,batch=null) {	// change lecture ondrop
	let subject_event = get_subject_event(subject_event_id);
	// console.log(Boolean(batch));
	if (Boolean(batch)){
		batch_element = td.find("[batch_for="+batch+"]");
		button = batch_element.find(".event_name");
		// console.log(button);
		// faculty_div = batch_element.find(".faculty_name");
		// resource_div = batch_element.find(".resource_name");
		
		button.html(subject_event.subject_name);
		button.css("background-color",subject_event.color);
		
		// faculty_div.html(subject_event.faculty_name);
		// resource_div.html(resource);
	}else{
		button = td.find(".event_name");
		faculty_div = td.find(".faculty_name");
		resource_div = td.find(".resource_name");
		
		button.html(subject_event.subject_name);
		button.css("background-color",subject_event.color);
		
		faculty_div.html(subject_event.faculty_name);
		resource_div.html(resource);
	}
}


function change_to_prac_td(td,subject_batch) {	// change td to prac td
	pair = get_prac_pair(td);
	/////////////////////////////// pair [0] - prac_above ////////////////////////////
	pair[0].removeClass("lect");
	pair[0].addClass("prac prac_above");
	let colspan;
	has_batch = Boolean(subject_batch.length);
	if (has_batch)
		colspan = (12/subject_batch.length);
	else 
		colspan = 12;
	let string = `<div class="container text-center"><div class="row text-center">`;
	
	if (has_batch){	
		for (i in subject_batch){
			string += `
			<div class=" col-`+ colspan+`"batch_for=`+subject_batch[i].pk+`>
				<div class="row" >
					<div class="col p-0 pt-1 prac_texts batch_name pl-`+ colspan+`">`+ batches[i].fields.name +`</div>
				</div>
				<div class="row" style="overflow-x: auto;">
					<div class="col mt-2">
						<button class="btn-sm prac_mycol event_name border-0" style = "padding: 0 1px 0 1px !important;"></button>
					</div>
				</div>
			</div>
			`;
		}
	}else{	// put "class" instead of batch_id
		string += `
			<div class=" col-`+ colspan+`"batch_for = class>
				<div class="row" >
					<div class="col p-0 pt-1 prac_texts batch_name pl-`+ colspan+`"></div>
				</div>
				<div class="row" style="overflow-x: auto;">
					<div class="col mt-2">
						<button class="btn-sm prac_mycol event_name border-0"></button>
					</div>
				</div>
			</div>
			`;
	}
	string += `</div></div>`
	pair[0].html(string);


	/////////////////////////////// pair [1] - prac_below ////////////////////////////
	pair[1].removeClass("lect");
	pair[1].addClass("prac prac_below");
	string = `<div class="container text-center"><div class="row">`
	if (has_batch){
		for (i in subject_batch){
			string +=
			`<div class="col-`+ colspan+` batch_contents " batch_for=`+subject_batch[i].pk+`>
				<div class="row ml-0 text-center">
					<div class="col-12 p-0 pl-`+ colspan+` prac_texts faculty_name"></div>
					<div class="col-12 p-0 pl-`+ colspan+` prac_texts resource_name"></div>
				</div>
			</div>`
		}
	}else{	// put "class" instead of batch_id
		string += 
		`<div class="col-`+ colspan+` batch_contents " batch_for = class >
			<div class="row ml-0 text-center">
				<div class="col-12 p-0 pl-`+ colspan+` prac_texts faculty_name"></div>
				<div class="col-12 p-0 pl-`+ colspan+` prac_texts resource_name"></div>
			</div>
		</div>`;
	}
	string += `</div></div>`;
	pair[1].html(string);


	pair[0].addClass("filled");
	pair[1].addClass("filled");
}


function put_prac(td,subject_event_id,batch,resource){
	subject_event = get_subject_event(subject_event_id);
	pair = get_prac_pair(td);
	batch = batch?batch:"class";
	
	div_above = pair[0].find("[batch_for="+batch+"]");
	div_below = pair[1].find("[batch_for="+batch+"]");
	
	button = div_above.find(".event_name");
	faculty_div = div_below.find(".faculty_name");
	resource_div = div_below.find(".resource_name");
	
	button.html(subject_event.subject_name);
	button.css("background-color",subject_event.color);

	faculty_div.html(subject_event.faculty_name);
	resource_div.html(resource);
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
	$(".isBreak").parent().each(function (){
		$(this).last().addClass("break_last");
	});
	///////////////////////////// Time Table ///////////////////////
	$(".droppable").bind('contextmenu', function (e) {
		// Show contextmenu
		// let rect = $(this)[0].getBoundingClientRect();
		var left,top = e.pageY+5;
		if (e.pageX+$(".context-menu").width() >= screen.width){
			left = e.pageX - $(".context-menu").width();
		}else{
			left = e.pageX;
		}
		$(".context-menu").toggle(100).css({
		 top: top + "px",
		 left: left + "px"
		});
		$(".clear_td").attr("slot_id",get_slot($(this)).id);
		$(this).addClass("right_click_selected"); // 

		return false;
	});
	$(document).bind('contextmenu click',function(){
		$(".context-menu").hide();
		$(".right_click_selected").removeClass("right_click_selected");
		$("#txt_id").val("");
	});
	$('.context-menu').bind('contextmenu',function(){
		return false;
	});
	$(".clear_td").click(function(){
		slot_id = $(this).attr("slot_id")
		if (get_cell(slot_id).hasClass("prac")){
			let i = get_event_index_by_slot(slot_id);
			if (i){
				clear_td(get_cell(events[i].Slot_id));
				clear_td(get_cell(events[i].Slot_id_2));
				events = events.filter(e=>e.Slot_id_2 != slot_id && e.Slot_id != slot_id );
			}
			console.table(events);
		}else{
			let i = get_event_index_by_slot(slot_id);
			if (i){
				clear_td(get_cell(events[i].Slot_id));
				// clear_td(get_cell(events[i].Slot_id_2));
				events = events.filter(e=>e.Slot_id_2 != slot_id && e.Slot_id != slot_id );
			}
			console.table(events);
		}
	})

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
				// console.log(subject_event.not_available[i]);
				if (td.length && !td.hasClass("filled")){
					td.addClass("not_available_td");
				}
			}
			// for all the other_events td add not_available
			for (k in subject_event.other_events){
				var obj = subject_event.other_events[k]['fields']
				event_td = get_cell(obj.Slot_id);
				if (event_td && !event_td.hasClass("filled")){
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
				$(".droppable").each(function(){
					var cellIndex = $(this).index();
					var td_below = $(this).closest('.my_row').next().children().eq(cellIndex);
					if ($(this).hasClass("not_available_td") || td_below.hasClass("not_available_td")|| td_below.hasClass("isBreak") || !td_below.length || (($(this).hasClass("filled") || td_below.hasClass("filled")) && !$(this).hasClass("prac"))){ 
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
			}else{
				$(".droppable").each(function(){
					if ($(this).hasClass("filled")){
						$(this).addClass("not_available_td");
					}
				});
			}
		 },
		drag: function( event, ui ) {
		},
		stop: function( event, ui ) {
			$(".droppable").each(function(){
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
				let subject_event_id = ui.draggable.attr("subject_event_id");
				let is_prac = ui.draggable.attr("is_prac");

				$("#resources option").prop('disabled', false);
				// all the options are enabled and then the filled resources are disabled 
				$("#batches").next(".select2-container").show();
				$("#batches option").prop('disabled', true);
				$("#resources option[value=-1]").prop('disabled', 'disabled');

				let subject_batches = get_batches(subject_event_id,is_prac);

				for (i in slot.resources_filled){
					$("#resources option[value='"+String(slot.resources_filled[i])+"']").prop('disabled', 'disabled');
				}
				if (!is_prac){				// if lecture
					if (subject_batches) {	// lect_batch
						for (let i in subject_batches) {
							$("#batches option[value=" + subject_batches[i].pk.toString() + "]").prop('disabled', false);
						}
					}else{					// lect_class
						console.log("lect_class");
						$("#batches").next(".select2-container").hide();
					}
					$("#event_form").removeAttr("is_prac");
				}
				else{
					if (subject_batches) {	// lect_batch
						for (let i in subject_batches) {
							$("#batches option[value=" + subject_batches[i].pk.toString() + "]").prop('disabled', false);
						}
					}else{					// lect_class
						console.log("lect_class");
						$("#batches").next(".select2-container").hide();
					}
					$("#event_form").attr("is_prac",is_prac);
				}
				$("#event_form").attr("slot_id",slot.id);
				$("#event_form").attr("subject_event_id",subject_event_id);

				// console.log(get_batches(subject_event_id,is_prac));

				// console.log($("option[value = "+9+"]"));
				// $("#event_form").show();


				let rect = $(this)[0].getBoundingClientRect();
				var left,top = event.pageY+5;
				if (rect.right+100 >= screen.width){
					left = rect.left - $("#event_form").width();
				}else{
					left = rect.right - 10;
				}

				// console.log(td[0].getBoundingClientRect());
				// Show contextmenu
				$("#event_form").toggle(100).css({
					top: top + "px",
					left: left + "px"
				});
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
			subject_batch = get_batches(subject_event_id,is_prac);
			if (is_prac){
				if (subject_batch){	// if prac_batch
					temp_event = new event_class(String(get_slot(get_prac_pair(td)[0]).id),subject_event_id,batch,resource,String(get_slot(get_prac_pair(td)[1]).id));
					if (push_event(temp_event)){
						if (!td.html()){
							change_to_prac_td(td,subject_batch);
						}
						put_prac(td,subject_event_id,batch,resource_name);
					}
				}else{			// if prac_class
					temp_event = new event_class(String(get_slot(get_prac_pair(td)[0]).id),subject_event_id,null,resource,String(get_slot(get_prac_pair(td)[1]).id));
					if (push_event(temp_event)){
						if (!td.html()){
							change_to_prac_td(td,subject_batch);
						}
						put_prac(td,subject_event_id,resource_name,batch=null);
					}
				}
			}else if(!is_prac){
				if (subject_batch){	// if lect_batch
					temp_event = new event_class(slot_id,subject_event_id,batch,resource);
					if (push_event(temp_event)){
						if (!td.html()){
							change_to_lect_td(td,subject_batch);
						}
						put_lect(td,subject_event_id,resource_name,batch);
					}
				}else{				// if lect_class
					temp_event = new event_class(slot_id,subject_event_id,null,resource);
					if (push_event(temp_event)){
						if (!td.html()){
							change_to_lect_td(td,null);
						}
						put_lect(td,subject_event_id,resource_name,batch=null);
					}
				}
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