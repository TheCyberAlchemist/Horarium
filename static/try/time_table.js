//#region  ////////////// classes & arrays ///////////////////////
var slots = [];
class slot {
	constructor(id = 0, day = 0, timing = 0, resources_filled = 0) {
		this.id = id;
		this.day = day;
		this.timing = timing;
		this.resources_filled = resources_filled;
	}
}

var subject_events = [];
class subject_event {
	constructor(id = 0, subject_name, subject_id, prac_carried, lect_carried, faculty_id, not_available, other_events, color, faculty_name) {
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
	constructor(Slot_id, Subject_event_id, Batch_id, Resource_id, Slot_id_2 = null, locked = false, link) {
		this.Slot_id = Slot_id;
		this.Subject_event_id = Subject_event_id;
		this.Batch_id = Batch_id ? Batch_id : null;
		this.Resource_id = Resource_id ? Resource_id : null;
		this.Slot_id_2 = Slot_id_2 ? Slot_id_2 : null;
		this.locked = locked ? locked : false;
		this.link = link;
	}
	put_slots(Slot_id, Slot_id_2) {
		this.Slot_id = Slot_id;
		this.Slot_id_2 = Slot_id_2 ? Slot_id_2 : null;
	}
	put_batch_resource(Batch_id, Resource_id) {
		this.Batch_id = Batch_id ? Batch_id : null;
		this.Resource_id = Resource_id ? Resource_id : null;
	}
	put_link_locked(link, locked = false) {
		this.link = link ? link : null;
		this.locked = locked ? locked : false;
	}
	put_subject_event(Subject_event_id) {
		this.Subject_event_id = Subject_event_id;
	}
	is_prac() {
		if (this.Slot_id_2) return true;
		return false;
	}
}

var actions = [];
var undo_actions = [];
class event_action {
	constructor(type, event) {
		this.type = type;
		this.event = event;
	}
}
var batches = [];
var subjects = [];
//#endregion

//#region  ////////////// hotkeys ////////////////////////////////
hotkeys("ctrl+z,ctrl+y", function (event, handler) {
	switch (handler.key) {
		case "ctrl+z":
			undo();
			break;
		case "ctrl+y":
			redo();
			break;
	}
});
//#endregion

//#region  ////////////// get methods ////////////////////////////

function get_prac_pair(td) {
	// console.log(td);
	var td_below = td.closest(".my_row").next().children().eq(td.index());
	var td_above = td.closest(".my_row").prev().children().eq(td.index());
	if (td_below.length && !td_below.hasClass("isBreak")) {
		return [td, td_below];
	} else if (td_above.length && !td_above.hasClass("isBreak")) {
		return [td_above, td];
	}
}

function get_slot_by_td(td) {
	let day = td.index();
	let time = td.parent().attr("timing_id");
	// console.log(slots[0],day,time);
	for (i in slots) {
		// print(slots[i].day);
		if (slots[i].day == day && slots[i].timing == time) {
			return slots[i];
		}
	}
}

function get_subject_event(id) {
	// console.log(slots[0],day,time);
	for (j in subject_events) {
		if (subject_events[j].id == id) {
			return subject_events[j];
		}
	}
}

function get_subject_by_subject_event(subject_event){
	// returns the subject object related to the subject_event object

	return subjects.filter((e)=> e.fields.short==subject_event.subject_name)[0]
}

function get_respective_lect_prac_batch(subject_event_id, is_prac = false) {
	// if the subject has batch it returns the practical or lecture batches
	// only for change to lect and prac td
	let subject_id = get_subject_event(subject_event_id).subject_id;
	let temp = [];

	if (is_prac) {
		for (b in batches) {
			let batch = batches[b].fields;
			if (batch.subjects_for_batch.includes(subject_id) && batch.batch_for == "prac") {
				temp = batches.filter((e) => e.fields.batch_for == "prac");
				break;
			}
		}
	} else {
		// if (batch.subjects_for_batch.includes(subject_id)&& e.fields.subjects_for_batch.includes(subject_id))
		for (b in batches) {
			let batch = batches[b].fields;
			if (batch.subjects_for_batch.includes(subject_id) && batch.batch_for == "lect") {
				// console.log(batch)
				temp = batches.filter((e) => e.fields.batch_for == "lect");
				break;
			}
		}
	}
	if (temp.length) {
		return temp;
	}
	return false;
}

function get_batches_for_subject_event(subject_event_id, is_prac = false) {
	// get all the batches that consist the subject event(P/L)
	let subject_id = get_subject_event(subject_event_id).subject_id;
	let temp = [];

	for (i in batches) {
		let batch = batches[i].fields;
		if ((is_prac && batch.batch_for == "prac") || (!is_prac && batch.batch_for == "lect")) {
			// if the related subject prac or lect has the batch
			if (batch.subjects_for_batch.includes(subject_id)) temp.push(batches[i]);
		}
	}
	if (temp.length) {
		return temp;
	}
	return false;
}

function get_event_index_by_slot(slot) {
	for (i in events) {
		if (events[i].Slot_id == slot || events[i].Slot_id_2 == slot) {
			return i;
		}
	}
	return false;
}

function get_cell(slot_id) {
	let slot_obj;
	// console.log(slot_id);
	for (i in slots) {
		if (String(slots[i].id) == String(slot_id)) {
			slot_obj = slots[i];
		}
	}
	if (!slot_obj) return $("#kaibhi");
	let tr = $("[timing_id=" + String(slot_obj.timing) + "]");
	let td = tr.find(".my_col:nth-child(" + (slot_obj.day + 1) + ")");
	// console.log(String(slot_obj.timing),$("tr"));
	// print(tr);
	return td;
}

function get_all_locked_events() {
	return events.filter((e) => e.locked == true);
}

function get_resource_name_by_id(resource_id) {
	let resource = "";
	if (!resource_id){
		return ""
	}
	$("#resources option").each(function () {
		if ($(this).val() == resource_id) {
			resource = $(this).html();
			// console.log(resource);
		}
	});
	return resource.split('(')[0];
}

function get_all_filled_td() {
	// returns an array of all the filled slots using filled class
	return $(".filled");
}
//#endregion

//#region  ////////////// put methods ////////////////////////////
function put_json_in_table(json_data) {
	// console.table("obj-",json_data);
	if (!json_data["my_events"]) {
		//#region for algo2 and all the other functions
		for (i in json_data) {
			let obj = json_data[i];
			td = get_cell(obj.Slot_id);
			if (td.hasClass("locked")) {
				// if the slot is locked
				// console.log(td);
				continue;
			}
			temp_event = new event_class();
			temp_event.put_subject_event(obj.Subject_event_id);
			temp_event.put_slots(obj.Slot_id, obj.Slot_id_2);
			temp_event.put_batch_resource(obj.Batch_id, obj.Resource_id);
			// console.log(obj.link);
			temp_event.put_link_locked(obj.link, obj.locked);
			// if (obj.Subject_event_id == 20)
			// 	console.log(temp_event);
			let resource = obj.Resource_id;
			if (temp_event.Slot_id_2) {
				// if it is a practical
				// print(temp_event);
				if (push_event(temp_event)) {
					// console.log(td);
					if (!td.html()) {
						change_to_prac_td(td, get_respective_lect_prac_batch(obj.Subject_event_id, true));
					}
					put_prac(td, obj.Subject_event_id, obj.Batch_id, resource,obj.link);
				}
			} else {
				if (push_event(temp_event)) {
					if (!td.html()) {
						change_to_lect_td(td, get_respective_lect_prac_batch(obj.Subject_event_id, false));
					}
					put_lect(td, obj.Subject_event_id, resource, obj.Batch_id, obj.link);
				}
			}
			if (obj.locked) {
				let cell = get_cell(temp_event.Slot_id);
				// let locking_events = events.filter(e=> e.Slot_id == obj.Slot_id || e.Slot_id_2 == obj.Slot_id);
				if (temp_event.Slot_id_2) {
					get_prac_pair(cell).forEach((e) => e.addClass("locked"));
				} else {
					console.log(cell.hasClass("locked"));
					cell.addClass("locked");
				}
			}
		}
		//#endregion
	} else {
		//#region for algo3
		let events_json = json_data["my_events"];
		for (i in events_json) {
			let obj = events_json[i];
			td = get_cell(obj.Slot_id);
			if (td.hasClass("locked")) {
				// if the slot is locked
				// console.log(td);
				continue;
			}
			temp_event = new event_class();
			temp_event.put_subject_event(obj.Subject_event_id);
			temp_event.put_slots(obj.Slot_id, obj.Slot_id_2);
			temp_event.put_batch_resource(obj.Batch_id, obj.Resource_id);
			temp_event.put_link_locked(obj.link, obj.locked);
			let resource = obj.Resource_id;
			if (temp_event.Slot_id_2) {
				// if it is a practical
				// print(temp_event);
				if (push_event(temp_event)) {
					// console.log(td);
					if (!td.html()) {
						change_to_prac_td(td, get_respective_lect_prac_batch(obj.Subject_event_id, true));
					}
					put_prac(td, obj.Subject_event_id, obj.Batch_id, resource, obj.link);
				}
			} else {
				if (push_event(temp_event)) {
					if (!td.html()) {
						change_to_lect_td(td, get_respective_lect_prac_batch(obj.Subject_event_id, false));
					}
					put_lect(td, obj.Subject_event_id, resource, obj.Batch_id, obj.link);
				}
			}
			if (obj.locked) {
				let cell = get_cell(temp_event.Slot_id);
				// let locking_events = events.filter(e=> e.Slot_id == obj.Slot_id || e.Slot_id_2 == obj.Slot_id);
				if (temp_event.Slot_id_2) {
					get_prac_pair(cell).forEach((e) => e.addClass("locked"));
				} else {
					console.log(cell.hasClass("locked"));
					cell.addClass("locked");
				}
			}
		}
		//#endregion
	}
}

function put_data(slots_json, sub_events_json, batches, old_events_json, subjects_json) {
	for (i in slots_json) {
		temp_slot = new slot(slots_json[i].pk, slots_json[i].fields.day, slots_json[i].fields.Timing_id, slots_json[i].fields.resources_filled);
		slots.push(temp_slot);
	}
	// console.table(sub_events_json);
	// events_json = JSON.parse(events_json.replace(/&#34;/ig,'"',));
	for (i in sub_events_json) {
		obj = sub_events_json[i].fields;
		temp_sub_event = new subject_event(sub_events_json[i].pk, obj.Subject_name, obj.Subject_id, obj.prac_carried, obj.lect_carried, obj.Faculty_id, obj.not_available, obj.other_events, obj.Subject_color, obj.Faculty_name);
		subject_events.push(temp_sub_event);
		// console.log("put_data");
		if (obj.prac_carried) {
			update_card(temp_sub_event, true);
		}
		if (obj.lect_carried) {
			update_card(temp_sub_event, false);
		}
	}
	this.batches = batches;
	this.subjects = subjects_json;
	// console.table(old_events_json);
	$(document).ready(function () {
		put_json_in_table(old_events_json);
	});
	// console.table(events);
	// console.table(subjects);
}

function put_event_in_td(my_event, td) {
	// gets the event and td and auto-calls the respective change_to function
	if (my_event.Slot_id_2) {
		let subject_batch = get_respective_lect_prac_batch(my_event.Subject_event_id, (is_prac = true));
		if (!td.html()) {
			change_to_prac_td(td, subject_batch);
		}
		put_prac(td, my_event.Subject_event_id, my_event.Batch_id, my_event.Resource_id, my_event.link);
	} else {
		// if lect
		let subject_batch = get_respective_lect_prac_batch(my_event.Subject_event_id, (is_prac = false));
		if (!td.html()) {
			change_to_lect_td(td, subject_batch);
		}
		put_lect(td, my_event.Subject_event_id, my_event.Resource_id, my_event.Batch_id, my_event.link);
	}
}

//#endregion

//#region  ////////////// only functions /////////////////////////

function print(abc) {
	console.log(abc);
	return true;
}

function intersects(a1, a2) {
	// console.log(a1,a2);
	for (j in a1) {
		if (a1[j] && a2.includes(a1[j])) return true;
	}
	return false;
}

function arraysEqual(a1, a2) {
	return JSON.stringify(a1) == JSON.stringify(a2);
}

function uniq_slot_id(a) {
	"Returns the arr of unique events";
	var seen = {};
	return a.filter(function (item) {
		return seen.hasOwnProperty(item.Slot_id) ? false : (seen[item.Slot_id] = true);
	});
}

function update_card(subject_event, is_prac) {
	let event_arr = events.filter((e) => e.Subject_event_id == subject_event.id && Boolean(e.Slot_id_2) == is_prac);
	let event_arr_len = uniq_slot_id(event_arr).length;
	// let event_arr_len = Math.max(event_arr.length,uniq_slot_id(event_arr).length)
	let remaining, event_load;
	if (is_prac) {
		remaining = subject_event.prac_carried - event_arr_len;
		event_load = $(`[subject_event_id = ${subject_event.id}][is_prac = ${is_prac}] .remaining_load`);
		event_load.html(remaining);
		// subject_card.html() += parseInt(subject_card.html())
	} else {
		remaining = subject_event.lect_carried - event_arr_len;
		event_load = $(`[subject_event_id = ${subject_event.id}][is_lect = "true"] .remaining_load`).html(remaining);
	}
	let subject_card = event_load.parentsUntil("#accordion");
	let subject_load = subject_card.find(".total_remaining_load");
	total_load = 0;
	subject_card.find(".remaining_load").each(function () {
		total_load += parseInt($(this).html());
	});
	// console.log(total_load);
	// console.log(total_load,subject_card);
	subject_load.html(total_load);
}

function update_all_cards() {
	for (let j in subject_events) {
		// update_card(subject_events[j],)
		// console.log(subject_events[j]);
		if (subject_events[j].prac_carried) {
			update_card(subject_events[j], true);
		}
		if (subject_events[j].lect_carried) {
			update_card(subject_events[j], false);
		}
	}
}

function clear_form(form) {
	form.trigger("reset");
	form.find("select").each(function () {
		$(this).val("-1").trigger("change");
	});
}

function subject_event_has_load_remaining(event_obj, is_prac = false) {
	let subject_event_id = event_obj.Subject_event_id;
	let subject_event = get_subject_event(subject_event_id);
	let event_arr = events.filter((e) => e.Subject_event_id == subject_event_id && Boolean(e.Slot_id_2) == is_prac);
	event_arr = uniq_slot_id(event_arr);
	// only get the number of prac or lecture taken without considering batches events on same slot
	event_arr = event_arr.filter((e) => e.Slot_id != event_obj.Slot_id);
	// remove the events on the same slot too as to not consider it
	total_similar_events = event_arr.length;
	// console.log(total_similar_events)
	if (total_similar_events) {
		// event_arr
		if (event_arr[0].Slot_id_2) {
			// if it was a practical
			if (subject_event.prac_carried > total_similar_events) {
				return true;
			}
		} else {
			// if it was a lecture
			if (subject_event.lect_carried > total_similar_events) {
				return true;
			}
		}
	} else if (!total_similar_events) {
		// if no event is still there
		return true;
	}
	console.log(`max filled - ${subject_event.subject_name}`, is_prac);
	return false;
}

function subject_has_load_for_batch(subject_id, batch_id, is_prac) {
	let subject = subjects.filter((e) => e.pk == subject_id)[0].fields;
	// console.log(subject_id);
	if (is_prac && subject.prac_per_week) {
		let all_events_for_subject_in_same_batch = events.filter((e) => e.Slot_id_2 && e.Batch_id == batch_id && get_subject_event(e.Subject_event_id).subject_id == subject_id);
		// if (subject_id == 14)
		// console.log(all_events_for_subject_in_same_batch,subject.prac_per_week,all_events_for_subject_in_same_batch.length);
		if (subject.prac_per_week > all_events_for_subject_in_same_batch.length) {
			return true;
		}
	} else if (!is_prac && subject.lect_per_week) {
		let all_events_for_subject_in_same_batch = events.filter((e) => !e.Slot_id_2 && e.Batch_id == batch_id && get_subject_event(e.Subject_event_id).subject_id == subject_id);
		if (subject.lect_per_week > all_events_for_subject_in_same_batch.length) {
			return true;
		}
	}
	console.log(`max filled for batch ${batch_id} - ${subject.name}`, is_prac);
	return false;
}

function open_menu_in_event_div(event_div, e) {
	const td_div = event_div.parents(".droppable");
	const batch_id = event_div.attr("batch_for");
	if (!td_div.hasClass("locked")) {
		// Show contextmenu
		// let rect = $(this)[0].getBoundingClientRect();
		var left,
			top = e.pageY + 5;
		if (e.pageX + $(".context-menu").width() >= screen.width) {
			left = e.pageX - $(".context-menu").width();
		} else {
			left = e.pageX;
		}
		$(".context-menu")
			.toggle(100)
			.css({
				top: top + "px",
				left: left + "px",
			});
		console.log(get_slot_by_td(td_div))
		$("#clear_td").attr("slot_id", get_slot_by_td(td_div).id);
		$("#clear_td").attr("batch_id", batch_id ? batch_id : false);
		// $(this).addClass("right_click_selected"); //
	}
	return false;
}

//#endregion

//#region  ////////////// events manipulation ////////////////////

function push_event(temp_event) {
	// check for batches in event_counter too
	const debug = true; // for printing the method if
	let a2 = [temp_event.Slot_id, temp_event.Slot_id_2];
	let subject_event = get_subject_event(temp_event.Subject_event_id);
	let is_prac = Boolean(a2[1]);

	if (get_cell(temp_event.Slot_id).hasClass("locked")) {
		console.log("This cell is locked");
		return false;
	}

	if (!subject_event_has_load_remaining(temp_event, is_prac) || !subject_has_load_for_batch(subject_event.subject_id, temp_event.Batch_id, is_prac)) {
		console.log("max_filled", subject_has_load_for_batch(subject_event.subject_id, temp_event.Batch_id, is_prac));
		return false;
	}
	for (var i = events.length - 1; i >= 0; i--) {
		let a1 = [events[i].Slot_id, events[i].Slot_id_2];
		if (arraysEqual(a1, a2) && events[i].Subject_event_id == temp_event.Subject_event_id) {
			let b1 = events[i].Batch_id;
			let b2 = temp_event.Batch_id;
			if (b1 == b2) {
				if (debug) {
					console.log(events[i]);
					console.log("duplicate");
				}
				return false;
			} else {
				if (debug) console.log("multiple batch write prac1(b1)-prac1(b2)");
			}
		} else if (intersects(a1, a2)) {
			// if there is overwritting
			let b1 = events[i].Batch_id;
			let b2 = temp_event.Batch_id;
			if (b1 == b2) {
				// if lect-lect or prac(b1)-prac(b1)
				if (debug) console.log("lect-lect or prac(b1)-prac(b1)");
				events.splice(i, 1);
				clear_td(get_cell(a1[0]));
				clear_td(get_cell(a1[1]));
				update_all_cards();
			} else {
				if (b1 && b2) {
					// if both not null prac(b1)-prac(b2)
					if (debug) console.log("prac(b1)-prac(b2)");
				} else {
					// if lect-prac or prac-lect
					if (debug) console.log("prac-lect or lect-prac");
					events.splice(i, 1);
					clear_td(get_cell(a1[0]));
					clear_td(get_cell(a1[1]));
				}
			}

			// clear the old slot td
		}
	}
	events.push(temp_event);
	update_card(subject_event, is_prac);
	return true;
}

function undo() {
	let last_action = actions.pop(); // use when completed
	// let last_action = actions[actions.length - 1];
	if (!last_action)
		// if no undo is here
		return false;
	// my_event is an array
	let my_events = last_action.event;
	console.assert(Array.isArray(my_events), "The event is not array here ❌❌ :: ", console.stack);
	let temp_events;
	switch (last_action.type) {
		case "removed":
			// for adding the event if possible
			for (my_event of my_events) {
				if (push_event(my_event)) {
					let td = get_cell(my_event.Slot_id);
					put_event_in_td(my_event, td);
				}
			}
			undo_actions.push(new event_action("added", my_events));
			break;
		case "added":
			// handles itself wery well without having an array of events to undo
			my_event = my_events[0];
			temp_events = events.filter((e) => e.Slot_id != my_event.Slot_id || e.Subject_event_id != my_event.Subject_event_id);
			if (my_event.locked) {
				alert("the event is locked.");
				break;
			}
			totally_clear_all(false);
			put_json_in_table(temp_events);

			undo_actions.push(new event_action("removed", my_events));
			break;
		case "cleared_unlocked":
			temp_events = my_events;
			// console.log(temp_events);
			put_json_in_table(temp_events);
			undo_actions.push(new event_action("put_all_unlocked", temp_events));
			break;
		case "replaced_events_arr":
			undo_actions.push(new event_action("replaced_events_arr", events));
			totally_clear_all(false);
			put_json_in_table(my_events)
			break;
	}
	// console.log(undo_actions);
}

function push_into_action(action, is_redo = false) {
	actions.push(action);
	if (is_redo)
		// if not called by redo related functions
		return;
	undo_actions = [];
	// console.trace();
	// console.log("new action occured !!");
}

function redo() {
	// console.log(undo_actions);
	let last_undo = undo_actions.pop(); // use when completed
	// let last_undo = undo_actions[undo_actions.length - 1];
	if (!last_undo)
		// if no undo is here
		return false;
	let my_events = last_undo.event;
	console.assert(Array.isArray(my_events), "The event is not array here ", console.stack);
	let temp_events, cleared;
	switch (last_undo.type) {
		case "added":
			my_event = my_events[0];
			// handles itself well without array of events
			let temp_events = events.filter((e) => e.Slot_id != my_event.Slot_id || e.Subject_event_id != my_event.Subject_event_id);
			cleared = clear_all_unlocked_td(my_event, (push_action = false), (is_redo = true));
			// console.log(cleared);
			if (cleared) {
				put_json_in_table(temp_events);
				push_into_action(new event_action("removed", my_events), true);
			} else {
				undo_actions.push(last_undo); // if any event is locked push the action
			}
			break;
		case "removed":
			// for adding the event if possible
			for (my_event of my_events) {
				if (push_event(my_event)) {
					let td = get_cell(my_event.Slot_id);
					put_event_in_td(my_event, td);
				}
			}
			console.log("in redo removed :: ", my_events);
			push_into_action(new event_action("added", my_events), true);
			break;
		case "put_all_unlocked":
			cleared = clear_all_unlocked_td(my_events, (push_action = false), (is_redo = true));
			// console.log(cleared);
			if (cleared) {
				push_into_action(new event_action("cleared_unlocked", my_events), true);
			} else {
				undo_actions.push(last_undo);
			}
			break;
		case "replaced_events_arr":
			push_into_action(new event_action("replaced_events_arr", events), true);
			totally_clear_all(false);
			put_json_in_table(my_events)
			break;
	}
	// console.log(undo_actions);
}

function show_all() {
	console.table(events);
	console.table(actions);
	console.table(undo_actions);
}
//#endregion

//#region  ////////////// clear & locking functions //////////////

function clear_td(td, totally_clear_all = false) {
	// refresh the td
	// console.log("clear called");
	if (td.length) {
		if (!totally_clear_all && td.hasClass("locked")) return;
		if (totally_clear_all) td.removeClass("locked");
		td.html("");
		if (td.hasClass("prac")) {
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

function clear_batch_div(td, batch) {
	// console.log(td.find(""))
	batch_div = td.find(`[batch_for=${batch}]`);
	button = batch_div.find(".event_name");
	faculty_div = batch_div.find(".faculty_name");
	resource_div = batch_div.find(".resource_name");
	faculty_div.html("");
	resource_div.html("");
	button.html("");
	button.css({ backgroundColor: "transparent" });
	// console.log(faculty_div,resource_div,button);
	console.log(batch_div);
	// change as needed
}

// get the event logic to clear unlocked from the redo
function totally_clear_all(push_action = true) {
	for (let i in events) {
		clear_td(get_cell(events[i].Slot_id), true);
		if (events[i].Slot_id_2) {
			clear_td(get_cell(events[i].Slot_id_2), true);	
		}
	}
	if (push_action) {
		push_into_action(new event_action("totally_cleared", events))
	};
	events = [];
	update_all_cards();
	return true;
}

function clear_all_unlocked_td(my_events = false, push_action = true, is_redo = false) {
	// clears all the cards and the associated event entries
	// is you do not want to push into action then push_action = false

	function clear_html() {
		if (my_events.length > 1) {
			for (let i in my_events) {
				clear_td(get_cell(my_events[i].Slot_id));
				if (my_events[i].Slot_id_2) clear_td(get_cell(my_events[i].Slot_id_2));
			}
		} else {
			for (let i in events) {
				clear_td(get_cell(events[i].Slot_id));
				if (events[i].Slot_id_2) clear_td(get_cell(events[i].Slot_id_2));
			}
		}
		if (push_action)
			push_into_action(
				new event_action(
					"cleared_unlocked",
					events.filter((e) => !e.locked)
				),
				is_redo
			);
		events = events.filter((e) => e.locked);
		update_all_cards();
	}
	let latest_my_events = [];
	if (my_events.length > 1) {
		for (i in my_events) {
			for (j in events) {
				if (my_events[i].Subject_event_id == events[j].Subject_event_id && my_events[i].Slot_id == events[j].Slot_id) {
					latest_my_events.push(events[j]);
				}
			}
		}
	}
	// console.log(my_events,latest_my_events);
	if ((my_events.length > 1 && latest_my_events.filter((e) => e.locked).length) || my_events.locked) {
		Swal.fire({
			icon: "error",
			title: "Locked event found! ",
			text: "Locked event cannot be deleted. ",
		});
		return false;
	} else {
		clear_html();
		return true;
	}
}

function lock_event_by_td(td) {
	let slot = get_slot_by_td(td);
	let locking_events = events.filter((e) => e.Slot_id == slot.id || e.Slot_id_2 == slot.id);
	if (Boolean(locking_events.length) && Boolean(locking_events[0].Slot_id_2)) {
		get_prac_pair(td).forEach((e) => e.toggleClass("locked"));
	} else {
		td.toggleClass("locked");
	}
	for (i in locking_events) {
		locking_events[i].locked = !locking_events[i].locked;
		// console.log(locking_events[i]);
	}
}

function lock_all_events() {
	events.forEach(function (x) {
		x.locked = true;
	});
	get_all_filled_td().addClass("locked");
}

function unlock_all_events() {
	events.forEach(function (x) {
		x.locked = false;
	});
	get_all_filled_td().removeClass("locked");
}

//#endregion

//#region  ////////////// put lect and prac on td ////////////////

function change_to_lect_td(td, subject_batch) {
	let colspan;
	let string = "";
	// console.log(subject_batch);
	has_batch = Boolean(subject_batch);
	// console.log(has_batch);
	if (has_batch) {
		// if lect_batch
		colspan = parseInt(12 / subject_batch.length);
		string += `<div class="container-fluid lect_batch_container">`;
		string += `<div class="row my-auto text-center" >`;
		for (let i in subject_batch) {
			string +=
			 `<div class="event_divs mt-2 col-`+colspan+`" batch_for=`+subject_batch[i].pk+` >
				<button class="btn event_name lect_mycol mt-2 lect_batches" 
				style="width:20px;height:55px;color:white"></button>
			</div>`;
		}
		string += `</div></div>`;
	}else{
		string +=
		`<div class='event_divs mt-2 row p-2' batch_for = "class">
			<div class='col-12'>
				<button class='event_name btn mt-1 mb-1'style = 'color:white;'></button>
			</div>
			<div class='col-6 text-left faculty_name'></div>
			<div class='col-6 text-right resource_name'></div>
		</div>`;
	}
	td.html(string);
	td.addClass("filled");
}

function put_lect(td, subject_event_id, resource_id, batch = null, link="---") {
	// change lecture ondrop
	let subject_event = get_subject_event(subject_event_id);
	let resource_name = get_resource_name_by_id(resource_id);
	let subject = get_subject_by_subject_event(subject_event)
	let title_resource = resource_name?resource_name:"---"
	link = link?link:"---"
	console.log(Boolean(link));
	if (Boolean(batch)) {
		batch_element = td.find("[batch_for=" + batch + "]");
		button = batch_element.find(".event_name");
		// console.log(button);
		// faculty_div = batch_element.find(".faculty_name");
		// resource_div = batch_element.find(".resource_name");
		let title_resource = resource_name?resource_name:"---"
		button.html(subject_event.subject_name);
		button.attr("data-tippy-content",`Subject Name : ${subject.fields.name} <br>Resource : ${title_resource}\nFaculty : ${subject_event.faculty_name} \nLink : ${link}`);
		button.css("background-color", subject_event.color);

		// faculty_div.html(subject_event.faculty_name);
		// resource_div.html(resource);
	} else {
		button = td.find(".event_name");

		faculty_div = td.find(".faculty_name");
		resource_div = td.find(".resource_name");

		button.html(subject_event.subject_name);
		button.attr("title",`Subject Name : ${subject.fields.name} \nResource : ${title_resource}\nFaculty : ${subject_event.faculty_name} \nLink : ${link}`);
		button.attr("data-tippy-content",`Subject Name : ${subject.fields.name} <br>Resource : ${title_resource}\nFaculty : ${subject_event.faculty_name} \nLink : ${link}`);
		button.css("background-color", subject_event.color);

		faculty_div.html(subject_event.faculty_name);
		resource_div.html(resource_name);
	}
}

function change_to_prac_td(td, subject_batch) {
	// change td to prac td
	pair = get_prac_pair(td);
	/////////////////////////////// pair [0] - prac_above ////////////////////////////
	pair[0].removeClass("lect");
	pair[0].addClass("prac prac_above");
	let colspan;
	has_batch = Boolean(subject_batch.length);
	if (has_batch) colspan = parseInt(12 / subject_batch.length);
	else colspan = 12;
	let string = `<div class="container text-center mt-1">`;

	if (has_batch) {
		string += `<div class="row text-center">`;
		for (i in subject_batch) {
			string +=
			`
				<div class="event_divs col-` +
					colspan +
					`"batch_for=` +
					subject_batch[i].pk +
					`>
					<!--<div class="row" >
					</div>-->
					<div class="row">
						<div class="col mt-1">
							<div class="col p-0 pt-1 prac_texts batch_name pl-`+ colspan+`">`+ batches[i].fields.name +`</div>
							<button class="btn-sm prac_mycol event_name border-0" 
							style="color:white;background-color:transparent"></button>
							<div class="row ml-0 text-center prac_below_texts">
								<div class="col-12 p-0 pl-1 prac_texts faculty_name"></div>
								<div class="col-12 p-0 pl-1 prac_texts resource_name"></div>
							</div>
						</div>
					</div>
					<!--<div class="row ml-0 text-center prac_below_texts">
						<div class="col-12 p-0 pl-1 prac_texts faculty_name"></div>
						<div class="col-12 p-0 pl-1 prac_texts resource_name"></div>
					</div>-->
				</div>
			`;
		}
	} else {
		// put "class" instead of batch_id
		console.log("here in class prac");
		string +=
			`
		<div class="row" style="width:100%">
			<div class="event_divs col-` +
			colspan +
			`" batch_for = class>
				<div class="row" style="width:100%;padding-right:0px !important;">
					<div class="col mt-2" style="width: 100%;">
						<div class="col p-0 pt-1 prac_texts batch_name"> &nbsp;</div>
						<button class="btn-sm prac_mycol event_name border-0" 
						style="width:auto;padding:10px !important;color:white;background-color:transparent"></button>
						<div class="ml-0 text-center prac_below_texts">
							<div class="col-12 p-0 pl-1 prac_texts faculty_name"></div>
							<div class="col-12 p-0 pl-1 prac_texts resource_name"></div>
                    	</div>
					</div>					
				</div>
                <!--<div class="row ml-0 text-center prac_below_texts">
                    <div class="col-12 p-0 pl-1 prac_texts faculty_name"></div>
                    <div class="col-12 p-0 pl-1 prac_texts resource_name"></div>
                </div>-->
			</div>
			`;
	}
	string += `</div></div>`;
	pair[0].html(string);

	/////////////////////////////// pair [1] - prac_below ////////////////////////////
	pair[1].removeClass("lect");
	pair[1].addClass("prac prac_below");
	// pair[1].html(string);
	pair[0].addClass("filled");
	pair[1].addClass("filled");
}

function put_prac(td, subject_event_id, batch, resource_id,link = "---") {
	let subject_event = get_subject_event(subject_event_id);
	let resource_name = get_resource_name_by_id(resource_id);
	let subject = get_subject_by_subject_event(subject_event)
	pair = get_prac_pair(td);
	batch = batch ? batch : "class";

	div_above = pair[0].find("[batch_for=" + batch + "]");
	div_below = pair[1].find("[batch_for=" + batch + "]");

	faculty_div = div_above.find(".faculty_name");
	resource_div = div_above.find(".resource_name");

	faculty_div.html(subject_event.faculty_name);
	resource_div.html(resource_name);

	button = div_above.find(".event_name");

	title_resource = resource_name?resource_name:"---"

	asd = subject_event.subject_name.split("").join("<br>");
	button.html(asd);
	
	button.attr("data-tippy-content",`Subject Name : ${subject.fields.name} <br>Resource : ${title_resource}\nFaculty : ${subject_event.faculty_name} \nLink : ${link}`);
	button.css("background-color", subject_event.color);
	button.css("white-space", "pre-line");

}
//#endregion

//#region  ////////////// ready function /////////////////////////
global_var = 0;
$(document).ready(function () {
	
	// $("[rel='tooltip']").tooltip();

	update_all_cards();
	///////////////////////////// AJAX setup ///////////////////////
	var csrftoken = Cookies.get("csrftoken");
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
	}
	// Ensure jQuery AJAX calls set the CSRF header to prevent security errors
	$.ajaxSetup({
		beforeSend: function (xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
	});

	$(".isBreak")
		.parent()
		.each(function () {
			$(this).last().addClass("break_last");
		});

	///////////////////////////// right click menu ///////////////////////
	$(".droppable").on("contextmenu", ".event_divs", function (e) {
		return open_menu_in_event_div($(this), e);
	});
	// $(".event_divs").bind('contextmenu', function (e) {
	// });
	$(document).bind("contextmenu click", function () {
		$(".context-menu").hide();
		$(".right_click_selected").removeClass("right_click_selected");
		$("#txt_id").val("");
	});

	$(".context-menu").bind("contextmenu", function () {
		return false;
	});

	$(".open_menu").click(function () {
		console.log();
	});

	$("#clear_td").click(function () {
		const slot_id = $(this).attr("slot_id");
		let batch_id = $(this).attr("batch_id");
		if (batch_id === "false" || batch_id === "class") {
			batch_id = null;
		}
		global_var = batch_id;
		const all_events_on_slot = events.filter((e) => e.Slot_id == slot_id);
		const this_event = all_events_on_slot.filter((e) => e.Batch_id == batch_id);
		// global_var = [this_event];
		if (this_event.length == 1) {
			if (this_event[0].is_prac()) {
				if (all_events_on_slot.length == 1) {
					// if only one event is there
					clear_td(get_cell(this_event[0].Slot_id));
					clear_td(get_cell(this_event[0].Slot_id_2));
				} else {
					// if two or more events are there
					clear_batch_div(get_cell(this_event[0].Slot_id), batch_id);
				}
			} else {
				if (all_events_on_slot.length == 1) {
					// if only one event is there
					clear_td(get_cell(this_event[0].Slot_id));
				} else {
					// if two or more events are there
					clear_batch_div(get_cell(this_event[0].Slot_id), batch_id);
				}
			}
			// console.log(this_event[0].Subject_event_id)
			events = events.filter((e) => e != this_event[0]);
			// global_var = [get_subject_event(this_event[0].Subject_event_id),this_event[0].is_prac()]
			update_card(get_subject_event(this_event[0].Subject_event_id), this_event[0].is_prac());
			push_into_action(new event_action("removed", this_event));
		} else console.log("No event found 😢");
	});

	$("#edit_event").click(function () {
		// console.log("here");
		const slot_id = $("#clear_td").attr("slot_id");
		let batch_id = $("#clear_td").attr("batch_id");
		console.log(batch_id,slot_id)
		if (batch_id === "false" || batch_id === "class") {
			batch_id = null;
		}
		const this_event = events.filter((e) => e.Slot_id == slot_id && e.Batch_id == batch_id);
		if (this_event.length == 1) {
			$("#batches").next(".select2-container").hide(); // hide batch
			const slot = slots.filter((e) => e.id == slot_id);
			$("#resources option").prop("disabled", false);
			// all the options are enabled and then the filled resources are disabled

			globar_var = this_event;
			for (i in slot.resources_filled) {
				$("#resources option[value='" + String(slot.resources_filled[i]) + "']").prop("disabled", "disabled");
			}
			//give default values
			// console.log(this_event)

			let Resource_id = this_event[0].Resource_id ? String(this_event[0].Resource_id) : "-1";
			$("#resources").val(Resource_id).trigger("change");
			let link = this_event[0].link || "-1";
			if ($(`#links option[value='${link}']`).length > 0){
				// if the link already exists
				$("#links").val(link).trigger("change");
			}else{
				let newOption = new Option(link, link, true, true);
				// Append it to the select
				$('#links').append(newOption).trigger('change');
			}
			global_var = [link, Resource_id];
			let rect = get_cell(slot_id)[0].getBoundingClientRect();
			var left,
				top = event.pageY + 5;
			if (rect.right + 100 >= screen.width) {
				left = rect.left - $("#event_form").width();
			} else {
				left = rect.right - 10;
			}
			if (this_event[0].is_prac()) {
				$("#event_form").attr("is_prac", true);
			} else {
				$("#event_form").removeAttr("is_prac");
			}
			$("#event_form").attr("slot_id", this_event[0].Slot_id);
			$("#event_form").attr("subject_event_id", this_event[0].Subject_event_id);
			// console.log("1");
			$("#event_form")
				.toggle(100)
				.css({
					top: top + "px",
					left: left + "px",
				});
			$("#edit_submit").parent().show();
			$("#aform").parent().hide();
		} else {
			console.log("No event found 😢");
		}
	});

	$("#edit_submit").click(function () {
		const slot_id = $("#clear_td").attr("slot_id");
		let batch_id = $("#clear_td").attr("batch_id");
		if (batch_id === "false" || batch_id === "class") {
			batch_id = null;
		}
		const this_event = events.filter((e) => e.Slot_id == slot_id && e.Batch_id == batch_id);
		if (this_event.length == 1) {
			const resource = $("#resources").val();
			const link = $("#links").val();
			this_event[0].Resource_id = resource == -1 ? null : resource;
			this_event[0].link = link;
			/////////
			my_event = this_event[0];
			let td = get_cell(my_event.Slot_id);
			if (my_event.Batch_id) {
				// if we need to clear only the batch div
				clear_batch_div(td, my_event.Batch_id);
			} else {
				// if we need to clear the whole td
				clear_td(td);
			}

			put_event_in_td(my_event, td);
		} else {
			console.log("No event found 😢");
		}
		$("#edit_submit").parent().hide();
		$("#event_form").hide();
	});
	///////////////////////////// draggable/droppable ///////////////////////

	$(".draggable")
		.draggable({
			revert: true,
			cursor: "move",
			helper: "clone",
			// containment: $('body'),
			appendTo: "body",
			cursorAt: { top: 56, left: 56 },
			start: function (event, ui) {
				// get all the td in which the faculty is not_available
				let subject_event = get_subject_event($(this).attr("subject_event_id"));
				// for all the not_available td add not_available
				for (i in subject_event.not_available) {
					td = get_cell(subject_event.not_available[i]);
					// console.log(subject_event.not_available[i]);
					if (td.length && !td.hasClass("filled")) {
						td.addClass("not_available_td");
					}
				}
				// for all the other_events td add not_available
				for (k in subject_event.other_events) {
					var obj = subject_event.other_events[k]["fields"];
					event_td = get_cell(obj.Slot_id);
					if (event_td && !event_td.hasClass("filled")) {
						event_td.addClass("not_available_td");
						// event_td.html(obj.Division_id)
					}
					if (obj.Slot_id_2) {
						// if it is practical
						event_td_2 = get_cell(obj.Slot_id_2);
						if (!event_td_2.hasClass("filled")) {
							event_td_2.addClass("not_available_td");
							// event_td.html(obj.Division_id)
						}
					}
				}
				if ($(this).attr("is_prac")) {
					$(".droppable").each(function () {
						var cellIndex = $(this).index();
						var td_below = $(this).closest(".my_row").next().children().eq(cellIndex);
						if ($(this).hasClass("not_available_td") || td_below.hasClass("not_available_td") || td_below.hasClass("isBreak") || !td_below.length || (($(this).hasClass("filled") || td_below.hasClass("filled")) && !$(this).hasClass("prac"))) {
							// if below is not available or filled or is break then not viable
							if (!($(this).hasClass("available_td") || $(this).hasClass("isBreak"))) $(this).addClass("not_available_td");
						} else {
							//	all the available
							// console.log("helr");
							$(this).addClass("available_td");
							td_below.addClass("available_td");
							td_below.removeClass("not_available_td");
						}
					});
				} else {
					$(".droppable").each(function () {
						if ($(this).hasClass("filled") && $(this).hasClass("prac")) {
							// if the cell has a practical in it
							$(this).addClass("not_available_td");
						} else if ($(this).find(".event_divs").attr("batch_for") == "class") {
							// if lecture then
							// if the lect is for class
							$(this).addClass("not_available_td");
						}
					});
				}
			},
			drag: function (event, ui) {},
			stop: function (event, ui) {
				$(".droppable").each(function () {
					$(this).removeClass("not_available_td");
					$(this).removeClass("available_td");
				});
			},
		})
		.disableSelection();

	$(".droppable").droppable({
		// on hover
		over: function (event, ui) {},
		// on out
		out: function (event, ui) {},
		// on drop
		drop: function (event, ui) {
			if (!$(this).hasClass("not_available_td")) {
				// if faculty is available at this slot
				let td = $(this);
				var slot = get_slot_by_td(td);
				let subject_event_id = ui.draggable.attr("subject_event_id");
				let is_prac = ui.draggable.attr("is_prac");
				$("#resources").val("-1").trigger("change");
				$("#links").val("-1").trigger("change");
				$("#batches").val("-1").trigger("change");
				$("#resources option").prop("disabled", false);
				// all the options are enabled and then the filled resources are disabled
				$("#batches").next(".select2-container").show();
				$("#aform").parent().show();
				$("#batches option").prop("disabled", true);
				$("#resources option[value=-1]").prop("disabled", "disabled");

				let subject_batches = get_batches_for_subject_event(subject_event_id, is_prac);

				for (i in slot.resources_filled) {
					$("#resources option[value='" + String(slot.resources_filled[i]) + "']").prop("disabled", "disabled");
				}
				if (!is_prac) {
					// if lecture
					if (subject_batches) {
						// lect_batch
						for (let i in subject_batches) {
							$("#batches option[value=" + subject_batches[i].pk.toString() + "]").prop("disabled", false);
						}
					} else {
						// lect_class
						// console.log("lect_class");
						$("#batches").next(".select2-container").hide();
					}
					$("#event_form").removeAttr("is_prac");
				} else {
					if (subject_batches) {
						// prac_batch
						for (let i in subject_batches) {
							$("#batches option[value=" + subject_batches[i].pk.toString() + "]").prop("disabled", false);
						}
					} else {
						// prac_class
						// console.log("prac_class");/
						$("#batches").next(".select2-container").hide();
					}
					$("#event_form").attr("is_prac", is_prac);
				}
				$("#event_form").attr("slot_id", slot.id);
				$("#event_form").attr("subject_event_id", subject_event_id);

				// console.log(get_batches(subject_event_id,is_prac));

				// console.log($("option[value = "+9+"]"));
				// $("#event_form").show();

				let rect = $(this)[0].getBoundingClientRect();
				var left,
					top = event.pageY + 5;
				if (rect.right + 100 >= screen.width) {
					left = rect.left - $("#event_form").width();
				} else {
					left = rect.right - 10;
				}

				// console.log(td[0].getBoundingClientRect());
				// Show contextmenu
				$("#edit_submit").parent().hide();
				$("#event_form")
					.toggle(100)
					.css({
						top: top + "px",
						left: left + "px",
					});
			}
		},
	});
	///////////////////////////// form  ///////////////////////

	$("#aform").on("click", function () {
		const slot_id = $("#event_form").attr("slot_id");
		const is_prac = $("#event_form").attr("is_prac");
		const subject_event_id = $("#event_form").attr("subject_event_id");
		const td = get_cell(slot_id);
		const resource = $("#resources").val();
		let temp = $("#resources").find(":selected").val();
		const resource_id = temp == -1 ? null : temp.split('(')[0];

		const subject_batch = get_batches_for_subject_event(subject_event_id, is_prac);
		const type_batch = get_respective_lect_prac_batch(subject_event_id, is_prac);
		const batches = $("#batches").val();
		const link = $("#links").val();

		if (/*resource && */ Boolean(batches.length) === Boolean(subject_batch)) {
			// validation of resource and batch if present
			let temp_event = new event_class();
			if (is_prac) {
				const slot_pair = get_prac_pair(td);
				let temp_pushed_events = [];
				if (subject_batch) {
					// if prac_batch
					for (batch of batches) {
						temp_event.put_subject_event(subject_event_id);
						temp_event.put_slots(String(get_slot_by_td(slot_pair[0]).id), String(get_slot_by_td(slot_pair[1]).id));
						temp_event.put_link_locked(link);
						temp_event.put_batch_resource(batch, resource);
						if (push_event(temp_event)) {
							temp_pushed_events.push(temp_event);
							if (!td.html()) {
								change_to_prac_td(td, type_batch);
							}
							put_prac(td, subject_event_id, batch, resource_id, link);
						}
						temp_event = new event_class();
					}
					push_into_action(new event_action("added", temp_pushed_events));
				} else {
					// if prac_class
					temp_event.put_subject_event(subject_event_id);
					temp_event.put_slots(String(get_slot_by_td(slot_pair[0]).id), String(get_slot_by_td(slot_pair[1]).id));
					temp_event.put_batch_resource(null, resource);
					temp_event.put_link_locked(link);

					if (push_event(temp_event)) {
						push_into_action(new event_action("added", temp_event));
						if (!td.html()) {
							change_to_prac_td(td, []);
						}
						put_prac(td, subject_event_id, null, resource_id,link);
					}
				}
			} else if (!is_prac) {
				let temp_pushed_events = [];
				if (subject_batch) {
					// if lect_batch
					for (batch of batches) {
						temp_event.put_subject_event(subject_event_id);
						temp_event.put_slots(slot_id);
						temp_event.put_batch_resource(batch, resource);
						temp_event.put_link_locked(link);
						if (push_event(temp_event)) {
							temp_pushed_events.push(temp_event);
							if (!td.html()) {
								change_to_lect_td(td, type_batch);
							}
							put_lect(td, subject_event_id, resource_id, batch, link);
						}
						temp_event = new event_class();
					}
					push_into_action(new event_action("added", temp_pushed_events));
				} else {
					// if lect_class

					temp_event.put_subject_event(subject_event_id);
					temp_event.put_slots(slot_id);
					temp_event.put_batch_resource(null, resource);
					temp_event.put_link_locked(link);

					if (push_event(temp_event)) {
						push_into_action(new event_action("added", [temp_event]));
						if (!td.html()) {
							change_to_lect_td(td, null);
						}
						put_lect(td, subject_event_id, resource_id, null, link);
					}
				}
			} else return;
			// console.table(events);
		} else {
			console.log("Error in saving the data ");
			return;
		}
		$("#event_form").hide();

		return;
	});

	$("#cancel").on("click", function () {
		$("#event_form").hide();
	});
	//////////////////////////// double click locking ///////////////////////////

	$(".droppable").dblclick(function (e, t) {
		lock_event_by_td($(this));
		// console.log(get_all_locked_events());
	});
});

//#endregion

//#region  ////////////// ajax function //////////////////////////

function submited() {
	// console.log("JSON.stringify(events),1)");
	$.ajax({
		type: "post",
		data: JSON.stringify(events),
		success: function () {},
	});
}
function functABC() {
	console.log("asd");
	return new Promise(function (resolve, reject) {
		$.ajax({
			type: "post",
			url: "./algo3/",
			data: {
				locked_events: JSON.stringify(get_all_locked_events()),
				merging_events: get_mearging_batches(),
				resource_allocation: $("#resource_allocation").prop("checked"),
			},

			success: function (data) {
				push_into_action(new event_action("replaced_events_arr", events));
				totally_clear_all(false);	
				put_json_in_table(data);
				// events = data.my_events;
				console.log("Algo3 returned data :- ", data);
			},
			error: function (data) {
				console.log("Error :- ", data.responseJSON);
				// set swal2 here
			},
		});
	});
}

function call_algo() {
	// console.log(get_all_locked_events());
	//#region for algo2
	// $.ajax({
	// 	type: "post",
	// 	url: "./algo3/",
	// 	data: JSON.stringify(get_all_locked_events()),
	// 	success: function (data){
	// 		clear_all_unlocked_td();
	// 		// console.log(events);
	// 		put_json_in_table(data);
	//   }
	// });
	//#endregion
	//#region for algo3
	functABC()
		.then(function (data) {
			// Run this when your request was successful
			console.log(data);
		})
		.catch(function (err) {
			// Run this when promise was rejected via reject()
			console.log(err);
		});

	//#endregion
}
function get_mearging_batches() {
	unique = [];
	obj = {};
	$.each($("#batch_mearging input:checkbox"), function () {
		var myname = this.name;
		if ($.inArray(myname, unique) < 0) {
			if ($(`[name=${myname}]:checked`).length) {
				unique.push(myname);
			}
		}
	});
	for (inp_name of unique) {
		arr = [];
		$(`#batch_mearging [name=${inp_name}]:checked`).each(function () {
			arr.push($(this).val());
		});

		obj[inp_name] = arr;
	}
	return JSON.stringify(obj);
}

//#endregion

function a() {
	console.log(events);
	push_into_action(new event_action("replaced_events_arr", events));
	totally_clear_all(false);
	put_json_in_table({
		my_events: [
			{
				Slot_id: 226,
				Slot_id_2: 231,
				Batch_id: 52,
				Subject_event_id: 50,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 227,
				Slot_id_2: 232,
				Batch_id: 53,
				Subject_event_id: 50,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 228,
				Slot_id_2: 233,
				Batch_id: 54,
				Subject_event_id: 50,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 229,
				Slot_id_2: 234,
				Batch_id: 55,
				Subject_event_id: 50,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 230,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 50,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 241,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 50,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 242,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 50,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 226,
				Slot_id_2: 231,
				Batch_id: 56,
				Subject_event_id: 51,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 227,
				Slot_id_2: 232,
				Batch_id: 57,
				Subject_event_id: 51,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 228,
				Slot_id_2: 233,
				Batch_id: 52,
				Subject_event_id: 52,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 229,
				Slot_id_2: 234,
				Batch_id: 52,
				Subject_event_id: 52,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 245,
				Slot_id_2: 250,
				Batch_id: 53,
				Subject_event_id: 52,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 243,
				Slot_id_2: 248,
				Batch_id: 53,
				Subject_event_id: 52,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 226,
				Slot_id_2: 231,
				Batch_id: 54,
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 227,
				Slot_id_2: 232,
				Batch_id: 54,
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 228,
				Slot_id_2: 233,
				Batch_id: 55,
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 245,
				Slot_id_2: 250,
				Batch_id: 55,
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 229,
				Slot_id_2: 234,
				Batch_id: 56,
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 243,
				Slot_id_2: 248,
				Batch_id: 56,
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 244,
				Slot_id_2: 249,
				Batch_id: 57,
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 256,
				Slot_id_2: 261,
				Batch_id: 57,
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 235,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 247,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 246,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 53,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 227,
				Slot_id_2: 232,
				Batch_id: 52,
				Subject_event_id: 54,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 226,
				Slot_id_2: 231,
				Batch_id: 53,
				Subject_event_id: 54,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 229,
				Slot_id_2: 234,
				Batch_id: 54,
				Subject_event_id: 54,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 226,
				Slot_id_2: 231,
				Batch_id: 55,
				Subject_event_id: 55,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 227,
				Slot_id_2: 232,
				Batch_id: 56,
				Subject_event_id: 55,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 228,
				Slot_id_2: 233,
				Batch_id: 57,
				Subject_event_id: 55,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 257,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 55,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 258,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 55,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 259,
				Slot_id_2: "",
				Batch_id: "",
				Subject_event_id: 55,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 228,
				Slot_id_2: 233,
				Batch_id: 56,
				Subject_event_id: 56,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 245,
				Slot_id_2: 250,
				Batch_id: 57,
				Subject_event_id: 56,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 260,
				Slot_id_2: "",
				Batch_id: 60,
				Subject_event_id: 56,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 262,
				Slot_id_2: "",
				Batch_id: 60,
				Subject_event_id: 56,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 263,
				Slot_id_2: "",
				Batch_id: 60,
				Subject_event_id: 56,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 244,
				Slot_id_2: 249,
				Batch_id: 56,
				Subject_event_id: 57,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 245,
				Slot_id_2: 250,
				Batch_id: 56,
				Subject_event_id: 57,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 226,
				Slot_id_2: 231,
				Batch_id: 57,
				Subject_event_id: 57,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 243,
				Slot_id_2: 248,
				Batch_id: 57,
				Subject_event_id: 57,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 264,
				Slot_id_2: "",
				Batch_id: 60,
				Subject_event_id: 57,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 265,
				Slot_id_2: "",
				Batch_id: 60,
				Subject_event_id: 57,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 271,
				Slot_id_2: "",
				Batch_id: 60,
				Subject_event_id: 57,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 243,
				Slot_id_2: 248,
				Batch_id: 52,
				Subject_event_id: 58,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 244,
				Slot_id_2: 249,
				Batch_id: 52,
				Subject_event_id: 58,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 256,
				Slot_id_2: 261,
				Batch_id: 53,
				Subject_event_id: 58,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 272,
				Slot_id_2: 277,
				Batch_id: 53,
				Subject_event_id: 58,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 260,
				Slot_id_2: "",
				Batch_id: 58,
				Subject_event_id: 58,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 262,
				Slot_id_2: "",
				Batch_id: 58,
				Subject_event_id: 58,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 263,
				Slot_id_2: "",
				Batch_id: 58,
				Subject_event_id: 58,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 245,
				Slot_id_2: 250,
				Batch_id: 52,
				Subject_event_id: 59,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 229,
				Slot_id_2: 234,
				Batch_id: 53,
				Subject_event_id: 59,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 264,
				Slot_id_2: "",
				Batch_id: 58,
				Subject_event_id: 59,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 265,
				Slot_id_2: "",
				Batch_id: 58,
				Subject_event_id: 59,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 271,
				Slot_id_2: "",
				Batch_id: 58,
				Subject_event_id: 59,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 243,
				Slot_id_2: 248,
				Batch_id: 54,
				Subject_event_id: 60,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 244,
				Slot_id_2: 249,
				Batch_id: 54,
				Subject_event_id: 60,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 227,
				Slot_id_2: 232,
				Batch_id: 55,
				Subject_event_id: 60,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 256,
				Slot_id_2: 261,
				Batch_id: 55,
				Subject_event_id: 60,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 260,
				Slot_id_2: "",
				Batch_id: 59,
				Subject_event_id: 60,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 262,
				Slot_id_2: "",
				Batch_id: 59,
				Subject_event_id: 60,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 263,
				Slot_id_2: "",
				Batch_id: 59,
				Subject_event_id: 60,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 245,
				Slot_id_2: 250,
				Batch_id: 54,
				Subject_event_id: 61,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 243,
				Slot_id_2: 248,
				Batch_id: 55,
				Subject_event_id: 61,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 264,
				Slot_id_2: "",
				Batch_id: 59,
				Subject_event_id: 61,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 271,
				Slot_id_2: "",
				Batch_id: 59,
				Subject_event_id: 61,
				Resource_id: "",
				link: "",
			},
			{
				Slot_id: 265,
				Slot_id_2: "",
				Batch_id: 59,
				Subject_event_id: 61,
				Resource_id: "",
				link: "",
			},
		],
	});
}
