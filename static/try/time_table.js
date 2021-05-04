///////////////////////////////// classes & arrays /////////////////////////////////
var slots = [];
class slot{
	constructor(id = 0,day = 0,timing = 0,resources_filled=0){
		this.id = id;
		this.day = day;
		this.timing = timing;
		this.resources_filled = resources_filled;
	}
}

var subject_events = [];
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

var events = [];
class event_class {
	constructor(Slot_id,Subject_event_id,Batch_id,Resource_id,Slot_id_2=null,locked = false){
		this.Slot_id = Slot_id;
		this.Subject_event_id = Subject_event_id;
		this.Batch_id = Batch_id?Batch_id:null;
		this.Resource_id = Resource_id?Resource_id:null;
		this.Slot_id_2 = Slot_id_2?Slot_id_2:null;
		this.locked = locked?locked:false;
	}
}

var actions = [];
var undo_actions = [];
class event_action{
	constructor(type, event){
		this.type = type;
		this.event = event;
	}
}
var batches = [];
var subjects = [];
///////////////////////////////// hotkeys /////////////////////////////////
hotkeys('ctrl+z,ctrl+y', function (event, handler){
	switch (handler.key) {
	  case 'ctrl+z': undo();
		break;
	  case 'ctrl+y': redo();
		break;
	}
  });


///////////////////////////////// get methods /////////////////////////////////

function get_prac_pair(td){
	var td_below = td.closest('.my_row').next().children().eq(td.index());
	var td_above = td.closest('.my_row').prev().children().eq(td.index());
	if (td_below.length && !td_below.hasClass("isBreak")){
		return [td,td_below];
	}else if(td_above.length && !td_above.hasClass("isBreak")){
		return [td_above,td];
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

function get_all_locked_events(){
	return events.filter(e=>e.locked == true);
}


///////////////////////////////// put methods/////////////////////////////////
function put_json_in_table(json_data){
	// console.log("obj",json_data);
	for(i in json_data){
		let obj = json_data[i];
		// console.log(obj);
		temp_event = new event_class(obj.Slot_id,obj.Subject_event_id,obj.Batch_id,obj.Resource_id,obj.Slot_id_2,obj.locked);
		// console.log(temp_event);
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
		if (obj.locked){
			let cell = get_cell(temp_event.Slot_id);
			// let locking_events = events.filter(e=> e.Slot_id == obj.Slot_id || e.Slot_id_2 == obj.Slot_id);
			if (temp_event.Slot_id_2){
				get_prac_pair(cell).forEach(e=>e.addClass("locked"))
			}
			else{
				console.log(cell.hasClass("locked"));
				cell.addClass("locked");
			}
		}
	}
}

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
		if (obj.prac_carried){
			update_card(temp_sub_event,true);
		}if(obj.lect_carried){
			update_card(temp_sub_event,false);
		}

	}
	this.batches=batches;
	this.subjects = subjects_json;
	// console.table(old_events_json);
	put_json_in_table(old_events_json);
	// console.table(events);
	// console.table(subjects);
}

///////////////////////////////// only functions /////////////////////////////////

function print(abc){
	console.log(abc);
	return true;
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

function update_card(subject_event,is_prac) {
	let event_arr = events.filter(e => e.Subject_event_id==subject_event.id && Boolean(e.Slot_id_2) == is_prac);
	let remaining,event_load;
	if (is_prac){
		remaining = subject_event.prac_carried - event_arr.length;
		event_load = $(`[subject_event_id = ${subject_event.id}][is_prac = ${is_prac}] .remaining_load`);
		event_load.html(remaining);
		// subject_card.html() += parseInt(subject_card.html())
	}else{
		remaining = subject_event.lect_carried - event_arr.length;
		event_load = $(`[subject_event_id = ${subject_event.id}][is_lect = "true"] .remaining_load`).html(remaining);
	}
	let subject_card = event_load.parentsUntil("#accordion");
	let subject_load = subject_card.find(".total_remaining_load");
	// let subject_card.find(".remaining_load");
	total_load = 0;
	subject_card.find(".remaining_load").each(function() {
		total_load += parseInt($(this).html());
	});
	subject_load.html(total_load);
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

///////////////////////////////// events manipulation /////////////////////////////////

function push_event(temp_event){
	// check for batches in event_counter too

	let a2 = [temp_event.Slot_id,temp_event.Slot_id_2];
	let subject_event = get_subject_event(temp_event.Subject_event_id);
	let is_prac = Boolean(a2[1]);
 
	if (get_cell(temp_event.Slot_id).hasClass("locked")){
		console.log("This cell is locked");
		return false;
	}

	if (!subject_event_has_load_remaining(temp_event.Subject_event_id,is_prac) || !subject_has_load_for_batch(subject_event.subject_id,temp_event.Batch_id,is_prac)){
		console.log("max_filled");
		return false;
	}
	for(var i = events.length - 1;i >= 0 ;i--){
		let a1 = [events[i].Slot_id,events[i].Slot_id_2];
		if ( arraysEqual(a1,a2) && events[i].Subject_event_id == temp_event.Subject_event_id){
			console.log(events[i]);
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
	let caller = push_event.caller.name
	if (caller != "put_json_in_table" && caller != "undo" && caller != "redo"){	
		// if not called by put_event (i.e. regular push)
		actions.push(new event_action("added",temp_event));
	}
	update_card(subject_event,is_prac);
	return true;
}

function undo(){
	let last_action = actions.pop();		// use when completed
	// let last_action = actions[actions.length - 1];
	if (!last_action)	// if no undo is here
		return false;
	let my_event = last_action.event;
	let temp_events;
	switch(last_action.type){
		case "removed":
			if (push_event(my_event)){
				let td = get_cell(my_event.Slot_id);
				if (my_event.Slot_id_2){
					let subject_batch = get_batches(my_event.Subject_event_id,is_prac=true);
					if (!td.html()){
						change_to_prac_td(td,subject_batch);
					}
					put_prac(td,my_event.Subject_event_id,my_event.Batch_id,my_event.Resource_id);
				}else{	// if lect 
					let subject_batch = get_batches(my_event.Subject_event_id,is_prac=false);
					if (!td.html()){
						change_to_lect_td(td,subject_batch);
					}
					put_lect(td,my_event.Subject_event_id,my_event.Resource_id,my_event.Batch_id);
				}
				undo_actions.push(new event_action("added",my_event));
			}
			break;
		case "added":
			temp_events = events.filter(e=> e.Slot_id != my_event.Slot_id || e.Subject_event_id != my_event.Subject_event_id);
			// console.log(my_event);
			if (my_event.locked){
				alert("the event is locked.")
			}
			totally_clear_all(false);
			// console.log(my_event,temp_events);
			// events = temp_events;
			put_json_in_table(temp_events);
			// console.table(events);
			undo_actions.push(new event_action("removed",my_event));
			break;
		case "cleared_unlocked":
			temp_events = my_event;
			// console.log(temp_events);
			put_json_in_table(temp_events);
			undo_actions.push(new event_action("put_all_unlocked",temp_events));
			break;
	}
	// console.log(undo_actions);
}

actions.push = function actions_push() {		// if the action array is pushed then undo_actions should be refreshed
	// if (actions[actions.length - 1])
		console.log();
	if (JSON.stringify(actions[actions.length - 1]) !== JSON.stringify(arguments[0]))
		Array.prototype.push.apply(this, arguments);
	if (!(actions_push.caller.name == "redo" || ( actions_push.caller.caller && actions_push.caller.caller.name == "redo")))
		undo_actions = [];
	// console.log(undo_actions);
};

function redo(){
	// console.log(undo_actions);
	let last_undo = undo_actions.pop();		// use when completed
	// let last_undo = undo_actions[undo_actions.length - 1];
	if (!last_undo)	// if no undo is here
		return false;
	let my_event = last_undo.event;
	let temp_events,cleared;
	switch(last_undo.type){
		case "added":
			temp_events = events.filter(e=> e.Slot_id != my_event.Slot_id || e.Subject_event_id != my_event.Subject_event_id);
			cleared = clear_all_unlocked_td(my_event,false);
			console.log(cleared);
			// events = temp_events;
			if (cleared){
				put_json_in_table(temp_events);
				actions.push(new event_action("removed",my_event));
			}else{
				undo_actions.push(last_undo);
			}
			// console.table(events);
			break;
		case "removed":
			if (push_event(my_event)){
				let td = get_cell(my_event.Slot_id);
				if (my_event.Slot_id_2){
					let subject_batch = get_batches(my_event.Subject_event_id,is_prac=true);
					if (!td.html()){
						change_to_prac_td(td,subject_batch);
					}
					put_prac(td,my_event.Subject_event_id,my_event.Batch_id,my_event.Resource_id);
				}else{	// if lect 
					let subject_batch = get_batches(my_event.Subject_event_id,is_prac=false);
					if (!td.html()){
						change_to_lect_td(td,subject_batch);
					}
					put_lect(td,my_event.Subject_event_id,my_event.Resource_id,my_event.Batch_id);
				}
				actions.push(new event_action("added",my_event))
			}	
			break;
		case "put_all_unlocked":
			cleared = clear_all_unlocked_td(my_event,false);
			// console.log(cleared);
			if (cleared){
				actions.push(new event_action("cleared_unlocked",my_event));
			}else{
				undo_actions.push(last_undo);
			}
			break;
	}
	// console.log(undo_actions);
}

function show_all(){
	console.table(events);
	console.table(actions);
	console.table(undo_actions);
}
///////////////////////////////// clear functions /////////////////////////////////

function clear_td(td,totally_clear_all=false){		// refresh the td
	// console.log("clear called");
	if (td.length){
		if (!totally_clear_all && td.hasClass("locked"))
			return;
		if (totally_clear_all )
			td.removeClass("locked");
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
	return false;
}



// get the event logic to clear unlocked from the redo 
function totally_clear_all(push_action = true){
	for(let i in events){
		clear_td(get_cell(events[i].Slot_id),true);
		if (events[i].Slot_id_2)
			clear_td(get_cell(events[i].Slot_id_2),true);
	}
	if (push_action)
		actions.push(new event_action("totally_cleared",events));
	events = [];
	for(let j in subject_events){
		// update_card(subject_events[j],)
		// console.log(subject_events[j]);
		if (subject_events[j].prac_carried){
			update_card(subject_events[j],true);
		}if(subject_events[j].lect_carried){
			update_card(subject_events[j],false);
		}
	}
	return true;	
}

function clear_all_unlocked_td(my_events = false,push_action = true){		// refresh all the td
	function clear_html(){
		if (my_events.length > 1){
			for(let i in my_events){
				clear_td(get_cell(my_events[i].Slot_id));
				if (my_events[i].Slot_id_2)
					clear_td(get_cell(my_events[i].Slot_id_2));
			}
		}else{
			for(let i in events){
				clear_td(get_cell(events[i].Slot_id));
				if (events[i].Slot_id_2)
					clear_td(get_cell(events[i].Slot_id_2));
			}
		}
		actions.push(new event_action("cleared_unlocked",events.filter(e=>!e.locked)));
		events = events.filter(e=>e.locked);
		for(let j in subject_events){
			// update_card(subject_events[j],)
			// console.log(subject_events[j]);
			if (subject_events[j].prac_carried){
				update_card(subject_events[j],true);
			}if(subject_events[j].lect_carried){
				update_card(subject_events[j],false);
			}
		}
	}
	let latest_my_events = [];
	if (my_events > 1){
		for(i in my_events){
			for (j in events){
				if (my_events[i].Subject_event_id == events[j].Subject_event_id && my_events[i].Slot_id == events[j].Slot_id){
					latest_my_events.push(events[j]);
				}
			}
		}
	}
	// console.log(my_events,latest_my_events);
	if ((my_events.length > 1 && latest_my_events.filter(e=>e.locked).length) || my_events.locked ){
		Swal.fire({
			icon: 'error',
			title: 'Locked event found! ',
			text: 'Locked event cannot be deleted. '
		  })
		return false;
	}else{
		clear_html();
		return true;
	}
}

///////////////////////////////// put lect and prac on td /////////////////////////////////


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
			<div class='col-6 text-left faculty_name'></div>
			<div class='col-6 text-right resource_name'></div>
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
	asd = subject_event.subject_name.split("").join("<br>");
	button.html(asd);
	button.css("background-color",subject_event.color);

	faculty_div.html(subject_event.faculty_name);
	resource_div.html(resource);
}

///////////////////////////////// ready function /////////////////////////////////

$(document).ready (function () {
	
	///////////////////////////// AJAX setup ///////////////////////
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

	///////////////////////////// right click menu ///////////////////////

	$(".droppable").bind('contextmenu', function (e) {
		if (!$(this).hasClass("locked")){
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
		}
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
				events_removed = events.filter(e=>e.Slot_id_2 == slot_id || e.Slot_id == slot_id );
				events = events.filter(e=>e.Slot_id_2 != slot_id && e.Slot_id != slot_id );
				for (e in events_removed){
					update_card(get_subject_event(events_removed[e].Subject_event_id),true);
					actions.push(new event_action("removed",events_removed[e]));
				}
			}
			// console.table(events);
		}else{
			let i = get_event_index_by_slot(slot_id);
			if (i){
				clear_td(get_cell(events[i].Slot_id));
				// clear_td(get_cell(events[i].Slot_id_2));
				events_removed = events.filter(e=>e.Slot_id_2 == slot_id || e.Slot_id == slot_id );
				events = events.filter(e=>e.Slot_id_2 != slot_id && e.Slot_id != slot_id );
				for (e in events_removed){
					update_card(get_subject_event(events_removed[e].Subject_event_id),false);
					actions.push(new event_action("removed",events_removed[e]));
				}
			}
			// console.table(events);
		}
	})
	///////////////////////////// draggable/droppable ///////////////////////

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
						// console.log("lect_class");
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
			let subject_batch = get_batches(subject_event_id,is_prac);
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
						put_prac(td,subject_event_id,batch=null,resource_name);
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
			// console.table(events);
		}else{
			return;
		}
		$("#event_form").hide();
		
		return;
	});
	
	$("#cancel").on("click", function(){
		$("#event_form").hide();
	});
	//////////////////////////// double click locking ///////////////////////////
	$(".droppable").dblclick(function(e,t){
		let slot = get_slot($(this));
		let locking_events = events.filter(e=> e.Slot_id == slot.id || e.Slot_id_2 == slot.id);
		if (Boolean(locking_events.length) && Boolean(locking_events[0].Slot_id_2)){
			get_prac_pair($(this)).forEach(e=>e.toggleClass("locked"))
		}
		else{
			$(this).toggleClass("locked");
		}
		for (i in locking_events){
			locking_events[i].locked = !locking_events[i].locked;
			// console.log(locking_events[i]);
		}
		// console.log(get_all_locked_events());
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

function call_algo(){
	$.ajax({
		type: "post",
		url: "./algo/",
		data: JSON.stringify(get_all_locked_events()),

		success: function (data){
			clear_all_unlocked_td();
			console.log(events);
			put_json_in_table(data);
	  }
  });
}