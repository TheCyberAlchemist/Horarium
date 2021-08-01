function faculty_edit_called(id) {
	// console.log(id);
	$.ajax({
		type: "POST",
		data: {"pk": id},
		url: "./faculty_edit_called/",
		success: function (data) {
			for(field in data){
				$(`#faculty_form [name='${field}']`).val(data[field]);
			}
			$("#faculty_form").find(".select2_input").each(function(){
				$(this).trigger("change");
			});
			$("#faculty_form").find(".password").each(function(){
				$(this).removeAttr('required');
				$(this).attr('disabled', 'disabled');
			});
			$("#faculty_form_status").html("Update");
			$("#faculty_form_accordian").collapse("show");
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
			console.log(data)
			for(field in data){
				$(`#student_form [name='${field}']`).val(data[field]);
			}
			$("#student_form").find(".select2_input").each(function(){
				$(this).trigger("change");
			});
			$("#student_form").find(".password").each(function(){
				$(this).removeAttr('required');
				$(this).attr('disabled', 'disabled');
			});
			$("#student_form_status").html("Update");
			$("#student_form_accordian").collapse("show");

		},
	});
}

function clear_form(form){
	form.trigger("reset");
	form.find(".select2_input").each(function(){
		$(this).val("-1").trigger("change");
	});
	form.find(".password").each(function(){
		$(this).prop('required',true);
		$(this).removeAttr("disabled");
	});
	form.find("[name=pk]").each(function(){
		$(this).removeAttr("value");
	});
	$("#"+form.attr("id")+"_error").parent().hide()
	$("#"+form.attr("id")+"_error").html("")
}

$(document).ready ( function (){
	clear_form($("#student_form"));
	clear_form($("#faculty_form"));
	$("#student_form").submit(function (e) {
		e.preventDefault();
		$.ajax({
			type: "POST",
			url: "./add_update_student/",
			data: $("#student_form").serialize(), // serializes the form's elements.
			success: function(data)
			{
				$(".accordion-button").click()
				clear_form($("#student_form"));
			},
			error: function (data) {
				console.log(data.responseJSON);
				$("#student_form_error").parent().show()
				$("#student_form_error").html(data.responseJSON['error'])
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
				$(".accordion-button").click()
				clear_form($("#faculty_form"));
				// console.log(data);
			},
			error: function (data) {
				console.log(data.responseJSON);
				$("#faculty_form_error").parent().show()
				$("#faculty_form_error").html(data.responseJSON['error'])
			}
		});
	})
	$('#faculty_form_accordian').on('hidden.bs.collapse', function () {
		// student on collapse of form accordion
		$("#faculty_form_status").html("Add");
		clear_form($("#faculty_form"));
	});
	$('#student_form_accordian').on('hidden.bs.collapse', function () {
		// student on collapse of form accordion
		$("#student_form_status").html("Add");
		clear_form($("#student_form"));
	})
})