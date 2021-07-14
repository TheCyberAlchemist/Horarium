f = [];
$( document ).ready(function() {
	$("#aform").submit(function (e) {
		// preventing from page reload and default actions
		e.preventDefault();
		// serialize the data for sending the form data.
		var serializedData = $(this).serialize();
		f.push(serializedData)
		console.log(f)
		// make POST ajax call
		$.ajax({
			type: 'POST',
			data:slots_json,
			success: function (){
			},
		})
	})
});
function return_tr(){
	var tr = document.createElement('tr');

	var name = document.createElement('td');
	name.innerHTML = '<label for="id_name"> Name : </label><input type="text" name="name" maxlength="10" required="" id="id_name">';
	tr.appendChild(name);

	var start_time= document.createElement('td');
	start_time.innerHTML = '<label for="start_time"> Start time : </label><input type="time" name="start_time" class="start_time">';
	tr.appendChild(start_time);

	var end_time= document.createElement('td');
	end_time.innerHTML = '<label for="end_time"> End time : </label><input type="time" name="end_time" class="end_time">';
	tr.appendChild(end_time);
	
	var is_break = document.createElement('td');
	is_break.innerHTML = '<label for="id_is_break">Is Break : </label><input type="checkbox" name="is_break" id="id_is_break">';
	tr.appendChild(is_break);

	var add_row = document.createElement('td');
	add_row.innerHTML = '<button type="button" class="add_row">ADD</button>';
	tr.appendChild(add_row);

	return tr;
}
$(document).ready ( function () {
	$(document).on("click", ".add_row" , function() {	
		var selected_tr = $(this)[0].parentElement.parentElement;;
		var tr = return_tr();
		selected_tr.parentNode.insertBefore(tr, selected_tr.nextSibling);
		selected_tr = $(this).parentsUntil("tbody").last();
		start_time = selected_tr.next().find(".start_time");
		start_time.val(function(){
			return selected_tr.find(".end_time").val();
		});
		start_time.attr('disabled','disabled');
		return tr;
	});
	$(document).on("change", ".end_time" , function() {
		selected_tr = $(this).parentsUntil("tbody").last();
		start_time = selected_tr.next().find(".start_time");
		start_time.val($(this).val());
	});
});
class slot{
	constructor(name = "",start_time = 0 ,end_time= 0,is_break=0){
		this.name = name;
		this.start_time = start_time;
		this.end_time = end_time;
		this.is_break = is_break;
	}
	//set slot(start_time,end_time,name){
		//  this.name = name;
	//  this.start_time = start_time;
	//  this.end_time = end_time;
	//}
	duration(){
		return this.end_time-this.start_time;
	}
	add(addend){
		this.start_time += addend;
		this.end_time += addend;
	}
	subtract(subtraend){
		this.start_time -= subtraend;
		this.end_time -= subtraend;
	}
}

var slots = [];
function submited(){

	for (var i = 0; i < document.getElementsByName("name").length ; i++){		
		start_time = document.getElementsByName("start_time")[i].value
		end_time = document.getElementsByName("end_time")[i].value
		name = document.getElementsByName("name")[i].value;
		is_break =  document.getElementsByName("is_break")[i].checked ? 1 : 0;
		temp = new slot(name,start_time,end_time,is_break)
		slots.push(temp);
	}
	$.ajax({
		type: "post",
		data: JSON.stringify(slots),
		success: function (){
		}
	});
	//   }
}