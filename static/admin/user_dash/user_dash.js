$(document).ready(function() {
	AjaxDatatableViewUtils.initialize_table(
	   $('#student_details'),
	   "./get_student_user_ajax/",
	   {
		   // extra_options (example)
		//    select: true,
		   processing: false,
		   autoWidth: false,
		   full_row_select: false,
		   scrollX: false,
	   }, {
		   // extra_data
		   // ...
	   },
   );
} );
function user_edit_called(id) {
	console.log(id);
	$.ajax({
		type:'POST',
		data: JSON.stringify(id),
		url:'./student_edit_called/',
		success: function(data) {
			$("#update_user_form [name='first_name']").val(data['first_name']);
			$("#update_user_form [name='last_name']").val(data['last_name']);
			$("#update_user_form [name='email']").val(data['email']);
		 }
	})
}