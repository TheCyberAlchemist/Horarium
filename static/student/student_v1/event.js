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
	var sec = 50;
	var i = 0;
	function main(){
		var d = new Date();
		// ct = new time(d.getHours(),d.getMinutes(),d.getSeconds());
		ct = new time(9,15,sec);
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
				st = new time(9,0,0);
				// ct = new time(9,45,0);
				et = new time(16,50,0);
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
		sec++;
		for(i in events){
			get_cell(events[i]).removeClass("td_gone");
		}
		for(i in events){
			// console.log(events,ct);
			if (events[i].ongoing(ct)){		// is an event is ongoing
				for(var j = 0;j < i ; j++){
					get_cell(events[j]).addClass("td_gone");
				}
				if (events[i].is_break){	// if a break is ongoing 
					$("#text").html(events[i].name + " ends in - " + get_counter(events[i],ct));
					console.log("The break is :: ",get_cell(events[i]));
					console.log( events[i].name + " ends in :: ",get_counter(events[i],ct));

				}else{						// if a class is ongoing 
					$("#text").html(events[i].name + " ends in - " + get_counter(events[i],ct));
					console.log("This lecture is :: ",get_cell(events[i]));
					console.log(events[i].name + " ends in :: ",get_counter(events[i],ct));
				}
				break;
			}else if (events[i].upcoming(ct)){		// is an event is upcoming
				for(var j = 0;j < i ; j++){
					get_cell(events[j]).addClass("td_gone");
				}
				$("#text").html(events[i].name + " starts in - " + get_counter(events[i],ct,true));
				console.log("This lecture is :: ",get_cell(events[i]));
				console.log(events[i].name + " starts in :: ",get_counter(events[i],ct,true));
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
				console.log("No upcoming lecture .");
			}
		}
	}
	interval = setInterval(main, 1000);
	$("#text").addClass("glow");
	main();

});

