function faculty_edit_called(id) {
	console.log(id);
	$.ajax({
		type: "POST",
		data: {"pk": id},
		url: "./faculty_edit_called/",
		success: function (data) {
			console.log(data);
			$("#faculty_form [name='first_name']").val(data["first_name"]);
			$("#faculty_form [name='last_name']").val(data["last_name"]);
			$("#faculty_form [name='email']").val(data["email"]);
		},
	});
}
function student_edit_called(id) {
	console.log(id);
	$.ajax({
		type: "POST",
		data: {"pk": id},
		url: "./student_edit_called/",
		success: function (data) {
			$("#student_form [name='first_name']").val(data["first_name"]);
			$("#student_form [name='last_name']").val(data["last_name"]);
			$("#student_form [name='email']").val(data["email"]);
		},
	});
}
function clear_form(form){
	form.trigger("reset");
	form.find(".select2_input").each(function(){
		$(this).val("-1").trigger("change");
	});
}
$(document).ready ( function (){
	$("#student_form").submit(function (e) {
		e.preventDefault();
		$.ajax({
			type: "POST",
			url: "./add_update_student/",
			data: $("#student_form").serialize(), // serializes the form's elements.
			success: function(data)
			{
				clear_form($("#student_form"));
			},
			error: function (data) {
				console.log(data.responseJSON);
			}
		});
	})
	$("#faculty_form").submit(function (e) {
		e.preventDefault();
		$.ajax({
			type: "POST",
			url: "./add_update_faculty/",
			data: $("#faculty_form").serialize(), // serializes the form's elements.
			success: function(data)
			{
				// clear_form($("#student_form"));
				console.log(data);
			},
			error: function (data) {
				console.log(data.responseJSON);
			}
		});
	})
})