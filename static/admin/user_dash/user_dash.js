$(document).ready(function() {
	AjaxDatatableViewUtils.initialize_table(
	   $('#student_details'),
	   "./get_student_user_ajax/",
	   {
		   // extra_options (example)
		   select: true,
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