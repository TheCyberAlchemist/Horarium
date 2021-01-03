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
	constructor(pk,start,end,name = null,is_break=false,open = true){
		this.pk = pk;
		this.name = name;
		this.start = start;
		this.end = end;
		this.open = open;
		this.is_break = is_break;
	}
	ongoing(ct){	//	returns if the lecture is ongoing
		if (!this.is_break){
			let s = this.start.delta(ct).tis;	// start - ct
			let e = this.end.delta(ct).tis;
			if (s < (INTERVAL)*60  && e > 0)
				return true;
			return false;
		}else{
			let s = this.start.delta(ct).tis;	// start - ct
			let e = this.end.delta(ct).tis;
			if (s < 0  && e > 0)
				return true;
			return false;
		}
	}
	upcomming(ct){	//	returns if the lecture starts in next 4 hrs
		let s = this.start.delta(ct).tis;
		let e = this.end.delta(ct).tis;
		if (s > 0 && e > 0 && s < (4 * 3600))
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
		temp_event = new event_class(e[i].pk,temp_start_time,temp_end_time,e[i].name);
		events.push(temp_event);
	}
	for (i in b){
		temp_start_time = new time();
		temp_start_time.time = b[i].start_time.split(":");
		temp_end_time = new time();
		temp_end_time.time = b[i].end_time.split(":");
		temp_event = new event_class(b[i].pk,temp_start_time,temp_end_time,b[i].name,true);
		events.push(temp_event);
	}	
	events.sort((a,b) => (a.start.tis > b.start.tis)? 1 : -1);
}

function get_cell(e){
	pk = e.pk;
	if (e.is_break){
		return $("th").map(function() {
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
	function main(){
		var d = new Date();
		// ct = new time(d.getHours(),d.getMinutes(),d.getSeconds());
		ct = new time(10,41);
		// console.log(events,ct);
		for(i in events){
			if (events[i].ongoing(ct)){		// is an event is ongoing
				if (events[i].is_break){	// if a break is ongoing 
					console.log("The break is :: ",get_cell(events[i]));
					console.log( events[i].name + " ends in :: ",get_counter(events[i],ct));
				}else{						// if a class is ongoing 
					console.log("This lecture is :: ",get_cell(events[i]));
					console.log(events[i].name + " ends in :: ",get_counter(events[i],ct));
				}
				break;
			}else if (events[i].upcomming(ct)){		// is an event is upcoming
				console.log("This lecture is :: ",get_cell(events[i]));
				console.log(events[i].name + " starts in :: ",get_counter(events[i],ct,true));
				break;
			}else{									// no upcoming events
				console.log("No upcoming lecture .");
				break;
			}

		}
	}
	main();
});

