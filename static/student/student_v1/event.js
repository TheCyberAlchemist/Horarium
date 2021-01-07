var events = [],breaks= [];
INTERVAL = 5;
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
		this.pk = pk;
		this.start = start;
		this.name = name;
		this.link = link;
		this.end = end;
		this.opened = opened;
		this.is_break = is_break;
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
	upcoming(ct){	//	returns if the lecture starts in next 4 hrs
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
		temp_event = new event_class(e[i].pk,temp_start_time,temp_end_time,e[i].link,e[i].name,false,opened);
		events.push(temp_event);
	}
	for (i in b){
		temp_start_time = new time();
		temp_start_time.time = b[i].start_time.split(":");
		temp_end_time = new time();
		temp_end_time.time = b[i].end_time.split(":");
		temp_event = new event_class(b[i].pk,temp_start_time,temp_end_time,null,b[i].name,true);
		events.push(temp_event);
	}	
	events.sort((a,b) => (a.start.tis > b.start.tis)? 1 : -1);
	// console.table(events);
}

function get_cell(e){
	console.log(e);
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

function get_counter(lect,ct,upcoming = false){	// returns list of [hr,min,sec]
	if (upcoming){
		t = lect.start.delta(ct).time
	}else{
		t = lect.end.delta(ct).time
	}
	return t[0]+" : " + t[1]+" : " + t[2];
}

$(document).ready (function () {
	var sec = 0;
	var i = 0;
	function main(){
		// sec++;
		var d = new Date();
		ct = new time(d.getHours(),d.getMinutes(),d.getSeconds());
		// ct = new time(11,10,sec);
		/////////////////// progress-bar /////////////////////////////
		if (i == 0) {
			i = 1;
			var elem = document.getElementById("myBar");
			var width = 1;
			var elem1 = document.getElementById("ct");
			var width1 = 1;
			var id = setInterval(frame, 1000);
			function frame() {
				var d = new Date();
				// ct = new time(d.getHours(),d.getMinutes(),d.getSeconds());
				st = new time(9,15,0);
				// ct = new time(9,45,0);
				et = new time(17,00,0);
				w = (ct.delta(st).tis/et.delta(st).tis)*100;
				$("#ct").html(ct.hrs + " : " + ct.min+ " : " + ct.sec);
				if (w >= 100) {
					clearInterval(id);
					i = 0;
				} else {
					width++;
					elem.style.width = w + "%";
					elem1.style.width = w + "%";
				}
			}
		}
		/////////////////// main code /////////////////////////////		
		// console.log(events,ct);
		for(i in events){
			// console.log(events[i]);
			get_cell(events[i]).removeClass("td_gone");
		}
		for(i in events){
			if (events[i].ongoing(ct)){		// is an event is ongoing
				for(var j = 0;j < i ; j++){
					get_cell(events[j])
					.addClass("td_gone")
					.removeClass("active");
				}
				if (events[i].is_break){	// if a break is ongoing 
					$("#text").html(events[i].name + " ends in - " + get_counter(events[i],ct));
					// console.log("The break is :: ",get_cell(events[i]));
					// console.log( events[i].name + " ends in :: ",get_counter(events[i],ct));

				}else{						// if a class is ongoing 
					$("#text").html(events[i].name + " ends in - " + get_counter(events[i],ct));
					next = events[parseInt(i)+1];
					if (!(next.is_break || events[i].end.delta(next.start).tis))	// if up next
						$("#text").append("<br>Up Next - "+ next.name );
					get_cell(events[i]).addClass("td_active");
					if (!events[i].opened){
						if(events[parseInt(i)-1] && events[parseInt(i)-1].link != events[i].link){
							window.open(events[i].link, '_blank')
							events[i].opened = true;
							setWithExpiry("opened-"+events[i].pk,true,6*3600*1000);
						}
					}
					// console.log("This lecture is :: ",get_cell(events[i]));
					// console.log(events[i].name + " ends in :: ",get_counter(events[i],ct));
				}
				break;
			}else if (events[i].upcoming(ct)){		// is an event is upcoming
				for(var j = 0;j < i ; j++){
					get_cell(events[j]).addClass("td_gone");
				}
				$("#text").html(events[i].name + " starts in - " + get_counter(events[i],ct,true));
				// console.log("This lecture is :: ",get_cell(events[i]));
				// console.log(events[i].name + " starts in :: ",get_counter(events[i],ct,true));
				break;
			}else if(events[i].gone(ct) && i != events.length){
				continue;
			}else if (events[i].gone(ct) && i == events.length){
				for(var j = 0;j < i ; j++){
					get_cell(events[j]).addClass("td_gone");
				}
				$("#text").removeClass("glow");
				// console.log(events[i]);
				clearInterval(interval);
				$("#text").html("No upcoming lecture 😎");
				// console.log("No upcoming lecture .");
			}
		}
	}
	interval = setInterval(main, 1000);
	$("#text").addClass("glow");
	main();

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
