var events = [],breaks= [];
const INTERVAL = 5;
const HOUR_VALUE = 3600 * 1000; 
class time{
	constructor(hrs = 0,min = 0 ,sec= 0){
		this.hrs = hrs;
		this.min = min;
		this.sec = sec;
		this.tis = (this.hrs * 3600) + (this.min * 60) + (this.sec);
	}
	set time(t){
		this.hrs = t[0];
		if (t[1] != null){
			this.min = t[1];
		}
		if (t[2] != null){
			this.sec = t[2];
		}
		this.tis = (this.hrs * 3600) + (this.min * 60) + (this.sec);
	}
	delta(ct){		//	returns a time object that has the
					//	 subtraction of the this time and current time
		var d_h = this.hrs - ct.hrs;
		var d_m = this.min - ct.min;
		var d_s = this.sec - ct.sec;
		var delta_t = new time(d_h,d_m,d_s);
		return delta_t;
	}
	get time(){		//	returns time in hrs:min:sec as an array
		var hr = Math.abs(parseInt(this.tis/3600));
        var temp = Math.abs(parseInt(this.tis % 3600));
        var min = Math.abs(parseInt(temp / 60));
		var sec = temp % 60;
		hr = (hr < 10) ? "0" + hr : hr
		min = (min < 10) ? "0" + min : min
		sec = (sec < 10) ? "0" + sec : sec
		return [hr,min,sec];
	}
	
}

class event_class{
	constructor(pk,start,end,link,name = null,is_break=false,opened = false){
	}
	put_pk_name_is_break(pk,name=null,is_break=false){
		this.pk = pk;
		this.name = name;
		this.is_break = is_break;
	}
	put_start_end_time(start,end){
		this.start = start;
		this.end = end;
	}
	put_faculty_short(faculty_short){
		this.faculty_short= faculty_short;
	}
	put_link_color_opened(link,color=null,opened=null){
		this.link = link;
		this.color = color;
		this.opened = opened;
	}
	ongoing(ct){	//	returns if the lecture is ongoing
		let s = this.start.delta(ct).tis;	// start - ct
		let e = this.end.delta(ct).tis;
		if (!this.is_break){
			if (s < (INTERVAL)*60  && e > 0)
				return true;
		}else{
			if (s < 0  && e > 0)
				return true;
		}
		return false;
	}
	upcoming(ct){
		if (!this.is_break){
			let s = this.start.delta(ct).tis;
			let e = this.end.delta(ct).tis;
			if (s > 0 && e > 0)
				return true;
		}
		return false;
	}
	gone(ct){	//	returns if the lecture starts in next 4 hrs
		let s = this.start.delta(ct).tis;
		let e = this.end.delta(ct).tis;
		if (e < 0)
			return true;
		return false;
	}
	is_break(){
		if (this.name)
			return true
		return false
	}
}

function put_events(e,b){
	for (i in e){
		temp_start_time = new time();
		temp_start_time.time = e[i].start_time.split(":");
		temp_end_time = new time();
		temp_end_time.time = e[i].end_time.split(":");
		opened = getWithExpiry("opened-"+e[i].pk);
		temp_event = new event_class();
		temp_event.put_pk_name_is_break(e[i].pk,e[i].name,false);
		temp_event.put_start_end_time(temp_start_time,temp_end_time);
		temp_event.put_faculty_short(e[i].faculty_short)
		temp_event.put_link_color_opened(e[i].link,e[i].color,opened);
		events.push(temp_event);
	}
	for (i in b){
		temp_start_time = new time();
		temp_start_time.time = b[i].start_time.split(":");
		temp_end_time = new time();
		temp_end_time.time = b[i].end_time.split(":");
		temp_event = new event_class();
		// temp_event = new event_class(b[i].pk,temp_start_time,temp_end_time,null,b[i].name,true);

		temp_event.put_pk_name_is_break(b[i].pk,b[i].name,true);
		temp_event.put_start_end_time(temp_start_time,temp_end_time);

		events.push(temp_event);
	}	
	events.sort((a,b) => (a.start.tis > b.start.tis)? 1 : -1);
	for (let j = events.length-1;j>=0;j--){
		if (events[j].is_break){
			events.splice(j,1);
		}else{
			break;
		}
	}
	for (let j = 0;j<events.length;j++){
		if (events[j].is_break){
			events.splice(j,1);
		}else{
			break;
		}
	}
	if (!events.length){ // if no event today
		$(".timeline_and_text").hide();
	}
	// console.table(events);
}

function get_cell(e){
	// console.log(e);
	pk = e.pk;
	if (e.is_break){
		return $("th").map(function() {
			// console.log($(this).attr('break_id'),parseInt(pk));
			if (parseInt($(this).attr('break_id')) == parseInt(pk)){
				return $(this);
			}
		})[0];
	}
	return $("td").map(function() {
		if (parseInt($(this).attr('event_id')) == parseInt(pk)){
			return $(this);
		}
	})[0];
}
function get_event_cell_by_id(event_id){
	return $("td").map(function() {
		if (parseInt($(this).attr('event_id')) == parseInt(event_id)){
			return $(this);
		}
	})[0];
	// console.log("asd");
}

function get_counter(lect,ct,upcoming = false){	// returns list of [hr,min,sec]
	if (upcoming){
		t = lect.start.delta(ct).time
	}else{
		t = lect.end.delta(ct).time
	}
	return t[0]+" : " + t[1]+" : " + t[2];
}

function toggle_theme() {
    var el1 = document.getElementById("light"),
      el2 = document.getElementById("dark");
	//   console.log("hi");
    if (el1.disabled) {   // if dark
      localStorage.setItem("theme", "");
      el1.disabled = false;
      el2.disabled = "disabled";
    } else {              // if light
      el1.disabled = "disabled";
      el2.disabled = false;
      localStorage.setItem("theme", "dark");
    } 
}

function get_event_by_id(pk){
	for(let e of events){
		if (e.pk == pk){
			return e;
		}
	}

}

function get_subject_by_id(id){
	for(let s of mandatory_subjects){
		if (s.id == id){
			return s;
		}
	}
}

let mandatory_subjects,meta_data;
function remove_mandatory_subject(subject_id){
	mandatory_subjects = mandatory_subjects.filter(s=>s.id !=subject_id);
}
function open_page_link(link=null,event_id,on_click=false){
	/**
		opens the link if pop-up is allowed else shows error
		also sets the cookie for the event_id
	*/
	if (link){
		if (!getWithExpiry("opened-"+event_id) || on_click){
			// if not already opened or if clicked
			let popUp = window.open(link, '_blank');
			if (popUp == null || typeof(popUp)=='undefined') { 	
				if (!getWithExpiry("link not opened pop-up allow")){	
					pop_up_warning();
					setWithExpiry("link not opened pop-up allow",true,3 * HOUR_VALUE);
				}
			}
			else if (on_click){	
				// if link is clicked then it will not open automatically for 2:10 hours
				setWithExpiry("opened-"+event_id,true,(2*HOUR_VALUE)+10);
			}else{
				// if opened automatically then 6 
				console.log(event_id);
				setWithExpiry("opened-"+event_id,true,6*HOUR_VALUE);
			}
		}
	}
}
function pop_up_warning(){
	Swal.fire(
		'<strong>Please allow pop-up</strong>',
		'Allow pop-ups so we can open your links automatically on time.',
		'warning'
	)
}
var sec = 55;
global_time = new time(8,10,sec);
//#region time related stuff
function runAtMidnight(fn){
	var midnight = new Date();
	function getRandomInt(min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
	}
	let refresh_mins = getRandomInt(0,10)
	let refresh_secs = getRandomInt(0,59)
	midnight.setHours(24, refresh_mins, refresh_secs, 0);
	var timeUntilMidnight = midnight.getTime() - Date.now();
	setTimeout(fn, timeUntilMidnight);
}
function put_events_on_timeline(){
	// for (let i in events){
	// 	events[i].start_time
	// }
	// console.table(events);
	for (let i in events){
		if (!events[i].is_break){
			$("#myProgress").append(
				`<div id="timeBar_left">
				<span class="text-left">`+events[i].start.hrs+":"+events[i].start.min+`</span>
				</div>`
			);
			st = events[i].start;
			break;
		}
	}
	for (let i=events.length-1;i>=0;i--){
		if (!events[i].is_break){
			$("#myProgress").append(
				`<div id="timeBar_right">
				<span class="text-right">`+events[i].end.hrs+":"+events[i].end.min+`</span>
				</div>`
			);
			et = events[i].end;
			break;
		}
	}
	for (let i in events){
		let w;
		if (events[i].start == st && events[i].end != et){		// if the first element is here
			w = (events[i].end.delta(st).tis/et.delta(st).tis)*100;
			temp_st_end = events[i].end.tis;
			$("#myProgress").append(
				`<div id="timeBar" style="width:`+w+`%">
				<span class="text">`+events[i].end.hrs+":"+events[i].end.min+`</span>
				<div class="circles"></div>
				</div>`
				);
			// console.log(events[parseInt(i)+1].start.delta(st).tis);
		}else if (events[i].end == et && events[i].start != st){	// if last event is here
			w = (events[i].start.delta(st).tis/et.delta(st).tis)*100;
			$("#myProgress").append(
				`<div id="timeBar" style="width:`+w+`%">
				<span class="text">`+events[i].start.hrs+":"+events[i].start.min+`</span>
				<div class="circles"></div>
				</div>`
			);
			break;
		}else if(events[i].start.delta(st).tis > 0 && events[i].start.tis != temp_st_end){
			w = (events[i].start.delta(st).tis/et.delta(st).tis)*100;
			// console.log(w,events[i].start,temp_st_end);
			$("#myProgress").append(
				`<div id="timeBar" style="width:`+w+`%">
				<span class="text">`+events[i].start.hrs+":"+events[i].start.min+`</span>
				<div class="circles"></div>
				</div>`
			);
		}
	}
	// console.log(events[0].start);
}
var progress_bar_counter = 0
var last_popped_event;
let first_main_call = true;
function main(){
	var d = new Date();
	ct = new time(d.getHours(),d.getMinutes(),d.getSeconds());
	// ct = new time(10,12,sec);
	// ct = global_time;
	/////////////////// progress-bar /////////////////////////////
	if (progress_bar_counter % 60 == 0){
		myvar = 0;
		if (myvar == 0 && ct.delta(et).tis < 0 && ct.delta(st).tis > 0) {
			// console.log("hi");
			myvar = 1;
			var elem = document.getElementById("myBar");
			var elem1 = document.getElementById("ct");
			var elem2 = document.getElementById("round_ct");
			frame()
			function frame() {
				// var d = new Date();
				// ct = new time(d.getHours(),d.getMinutes(),d.getSeconds());
				// st = new time(9,15,0);
				// ct = new time(9,45,0);
				// et = new time(17,00,0);
				let e = false;
				for(let j in events){
					if (ct.delta(events[j].end).tis < 0 && ct.delta(events[j].start).tis > 0)
						e = events[j];
				}
				w = (ct.delta(st).tis/et.delta(st).tis)*100;
				// console.log(w);
				$("#ct").html(ct.time[0] + " : " + ct.time[1]);
				// $("#ct").html(ct.time[0] + " : " + ct.time[1] + "<br>" + e.name);
				if (w >= 100) {
					clearInterval(id);
					myvar = 0;
				} else {
					elem.style.width = w + "%";
					elem1.style.width = w + "%";
					elem2.style.width = w + "%";
				}
			}
		}else{
			document.getElementById("myBar").style.width = 0 + "%";
			// $("#myProgress").hide();
		}
		
	}
	// sec++;
	/////////////////// main code /////////////////////////////		
	// console.log(events,ct);
	for(let i in events){
		// console.log(events[i],1);
		get_cell(events[i]).removeClass("td_gone");
	}
	// console.log("here");
	for(i in events){
		if (events[i].ongoing(ct)){		// is an event is ongoing
			$(".timeline_and_text").show();
			for(var j = 0;j < i ; j++){
				// for all events that have been completed
				get_cell(events[j])
				.addClass("td_gone")
				.removeClass("td_active");
			}
			if (events[i].is_break){	// if a break is ongoing 
				$("#text").html(events[i].name + " ends in - " + get_counter(events[i],ct));
				next = events[parseInt(i)+1];
				if (next){
					if(!(next.is_break || events[i].end.delta(next.start).tis)){	
						// if not a break and next event is perfectly after this 
						$("#text").append("<br>Up Next - "+ next.name );
						if (next.ongoing(ct) && !next.opened){
							console.log("link open called",next)
							open_page_link(next.link,next.pk);
							next.opened = true;
						}
					}

				}
				// console.log("The break is :: ",get_cell(events[i]));
				// console.log( events[i].name + " ends in :: ",get_counter(events[i],ct));

			}else{						// if a class is ongoing 
				// console.log(events[i])
				$("#text").html(events[i].name + " ends in - " + get_counter(events[i],ct));

				next = events[parseInt(i)+1];
				if (next && !(next.is_break || events[i].end.delta(next.start).tis))	// if up next
					$("#text").append("<br>Up Next - "+ next.name );
				get_cell(events[i]).addClass("td_active");
				if (!events[i].opened){
					if(parseInt(i) == 0 || (parseInt(i) != 0 && (events[parseInt(i)-1].link != events[i].link || (events[parseInt(i)-1].link == events[i].link && !(events[parseInt(i)-1].opened))))){
						// if first event OR
						// if last events link is not same as this one OR
						// if same but this last one is not opened
						open_page_link(events[i].link,events[i].pk);
						events[i].opened = true;
					}
				}
				// console.log("This lecture is :: ",get_cell(events[i]));
				// console.log(events[i].name + " ends in :: ",get_counter(events[i],ct));
			}
			break;
		}else if (events[i].upcoming(ct)){		// is an event is upcoming
			$(".timeline_and_text").show();
			console.log("here upcoming");
			for(var j = 0;j < i ; j++){
				get_cell(events[j]).addClass("td_gone");
			}
			$("#text").html(events[i].name + " starts in - " + get_counter(events[i],ct,true));
			// console.log("This lecture is :: ",get_cell(events[i]));
			// console.log(events[i].name + " starts in :: ",get_counter(events[i],ct,true));
			break;
		}else if (events[i].gone(ct) && i == events.length-1){
			for(var j = 0;j < i ; j++){
				get_cell(events[j]).addClass("td_gone");
			}
			// console.log(events[i]);
			clearInterval(interval);
			$("#text").html("No upcoming lectures ... ");
			$(".timeline_and_text").hide();
			// console.log("No upcoming lecture .");
		}
	}
}
//#endregion.
jQuery(function () {

	//#region  ////////////// Browser Agent //////////////
	function userAgent() {
		let userAgentString = navigator.userAgent;
		// Detect Chrome
		let chromeAgent = userAgentString.indexOf("Chrome") > -1;
		// Detect Safari
		let safariAgent = userAgentString.indexOf("Safari") > -1;
		//Detect Firefox
		let firefoxAgent = userAgentString.indexOf("Firefox") > -1;
		
		console.log("firefox : " +firefoxAgent+" Chrome : " +chromeAgent+" Safari : " +safariAgent)
		// Discard Safari since it also matches Chrome
		if ((chromeAgent) && (safariAgent)) safariAgent = false;
		if(firefoxAgent) {
			$("body").addClass("safari");
		}
		console.log(firefoxAgent,chromeAgent,safariAgent)
	}
	//#endregion
	
	//#region  ////////////// pop-up allowance //////////////
	if (!getWithExpiry("pop-up info")){
		pop_up_warning();
		setWithExpiry("pop-up info",true,1000 * HOUR_VALUE);
	}
	//#endregion
	let st,et;
	var i = 0;
	//#region  ////////////// boiler-plate //////////////
	AOS.init({
        offset : 150,
    });
	let cookie = localStorage.getItem("theme") || "";
	// console.log(cookie,"asdasd");
	if (cookie === ""){
		$("#slider1").prop("checked",true);
			// console.log("hi");
		toggle_theme();
	}
	//#endregion

	
	//#region  ////////////// time-related stuff //////////////
	runAtMidnight(window.location.reload);
	put_events_on_timeline();
	if (events.length){
		interval = setInterval(main, 1000);
		main();
		first_main_call = false;
	}
	//#endregion

/* #region  Righ-click context menu */
	// Trigger action when the contexmenu is about to be shown
	$("#change_resource").select2();
	$("td").bind("contextmenu", function (event) {
	// Avoid the real one
	event.preventDefault();
	// Show contextmenu
	$(".custom-menu")
		.finish()
		.toggle(100)
		// In the right position (the mouse)
		.css({
		top: event.pageY + "px",
		left: event.pageX + "px",
		});
	});

	// If the document is clicked somewhere
	$("table").bind("mousedown", function (e) {
	// If the clicked element is not the menu
	if (!$(e.target).parents("td.align-middle").length) {
		// Hide it
		$(".custom-menu").hide();
	}
	});
	$("td").bind("contextmenu", function (e) {
	// If the clicked element is not the menu
	if (!$(e.target).parents("td.align-middle").length) {
		// Hide it
		$(".custom-menu").hide();
	}
	});

	// If the menu element is clicked
	$(".custom-menu li").click(function () {
	// This is the triggered action name
	// switch($(this).attr("data-action")) {

	//     // A case for each action. Your actions here
	//     case "first": alert("first"); break;
	//     case "second": alert("second"); break;
	//     case "third": alert("third"); break;
	// }

	// Hide it AFTER the action was triggered
	$(".custom-menu").hide(100);
	});
/* #endregion */

});

function setWithExpiry(key, value, ttl) {
	const now = new Date()

	// `item` is an object which contains the original value
	// as well as the time when it's supposed to expire
	const item = {
		value: value,
		expiry: now.getTime() + ttl,
	}
	localStorage.setItem(key, JSON.stringify(item))
}

function getWithExpiry(key) {
	const itemStr = localStorage.getItem(key)

	// if the item doesn't exist, return null
	if (!itemStr) {
		return null
	}

	const item = JSON.parse(itemStr)
	const now = new Date()

	// compare the expiry time of the item with the current time
	if (now.getTime() > item.expiry) {
		// If the item is expired, delete the item from storage
		// and return null
		localStorage.removeItem(key)
		return null
	}
	return item.value
}

