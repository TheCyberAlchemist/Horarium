JSON_DATA = {
		"first_name": "Dharmesh",
		"last_name": "Darji",
		"email": "ddharmesh@darji.com",
		"password1":"thatismyname",
		"password2":"thatismyname",
		"short": "DSD",
		"Designation_id": 1,
		"Shift_id": 6,
		"Department_id": 1,
		"total_load": 100,
		"can_teach": [
			11,12
		]
	}
		//"first_name": "Manav",
		//"last_name": "manav",
		//"email": "manav@mehta1.com",
		//"password1":"thatismyname",
		//"password2":"thatismyname",
		//"roll_no": "22",
		//"Institute_id": 1,
		//"Division_id": 4,
		//"prac_batch": 7,
		//"lect_batch": null
		
		//"pk":15,//for student
		//"pk":13,//for faculty

//API_URL = "../user_dash/1/faculty_edit_called/"
API_URL = "../user_dash/1/add_update_faculty/"
function send_ajax(){
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
	var locked = [
		{
			"Slot_id": "2",
			"Subject_event_id": "28",
			"Batch_id": null,
			"Resource_id": "1",
			"Slot_id_2": null,
			"locked": true,
			"link": "asd"
		},
		{
			"Slot_id": "7",
			"Subject_event_id": "29",
			"Batch_id": null,
			"Resource_id": "1",
			"Slot_id_2": null,
			"locked": true,
			"link": "None"
		}
	];
	// {
	// 	"Slot_id": "2",
	// 	"Subject_event_id": "28",
	// 	"Batch_id": null,
	// 	"Resource_id": "1",
	// 	"Slot_id_2": null,
	// 	"locked": true,
	// 	"link": "None"
	// }
	//console.log({
	//		"locked_events":JSON.stringify(locked),
	//		"merging_events":{"asd":"asd"},
	//	})
	$.ajax({
		url:API_URL,
		type: "post",
		data: JSON_DATA,
		success: function (data){
			document.getElementsByClassName("response")[0].textContent = JSON.stringify(data, undefined, 2);
		}
	});
}
document.getElementsByClassName("sent")[0].textContent = JSON.stringify(JSON_DATA, undefined, 2);
document.getElementsByClassName("url")[0].textContent = API_URL
//native javascript
hotkeys('space', function (event, handler){
	switch (handler.key) {
	case 'space': send_ajax();
		break;
	}
});