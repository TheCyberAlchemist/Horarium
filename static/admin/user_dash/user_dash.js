$(document).ready(function () {
	/* student datatable */ {
		let student_last_searched = false;
		$("#student_details").on("drawCallback", function (event, table) {
			$("tr .gixi").each(function () {
				$(this).gixi();
			});
		});
		AjaxDatatableViewUtils.initialize_table(
			$("#student_details"),
			"./get_student_user_ajax/",
			{
				// extra_options (example)
				//    select: true,
				// responsive: true,
				processing: false,
				autoWidth: false,
				full_row_select: false,
				scrollX: false,
				dom: "<'row'<'col-sm-12 col-md-8'l><'col-sm-12 col-md-4 p-1 bg-light rounded rounded-pill shadow-sm mb-4 search_div'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
			},
			{
				// extra_data
				// ...
			}
		);
		$("#student_details").on("draw.dt", function () {
			let initial_value = $("#pills-student .search_div input").val();
			$("#pills-student .search_div").html(`
				<div id="student_details_filter" class="dataTables_filter">
					<div class="input-group">
						<input type="search" placeholder="Global Search" aria-describedby="button-addon1" 
						class="form-control form-control-sm border-0 bg-light" id="global_search_box" style="box-shadow:none;outline:none" aria-controls="student_details">
						<div class="input-group-append">
							<button id="button-addon1" type="submit" class="btn btn-link text-primary" style="box-shadow:none;outline:none;padding:0;z-index:20"><i class="fa fa-search" style="transform:translateX(-10px)"></i></button>
						</div>
					</div>
				</div>`
			);
			$("#pills-student .search_div input").val(initial_value)
			if (student_last_searched)
				$("#pills-student .search_div input").focus();
			$("#pills-student .datatable-column-filter-row input").on("input", function () {
				student_last_searched = false;
			});
			$("#global_search_box").on("input", function () {
				student_last_searched = true;
				var table = $.fn.dataTable.Api($("#student_details"));
				table.search($(this).val()).draw();
			});
		});
	}
	/* faculty datatable */{
		let faculty_last_searched = false;
		$("#faculty_details").on("drawCallback", function (event, table) {
			$("tr .gixi").each(function () {
				$(this).gixi();
			});
		});
		AjaxDatatableViewUtils.initialize_table(
			$("#faculty_details"),
			"./get_faculty_user_ajax/",
			{
				// extra_options (example)
				//    select: true,
				// responsive: true,
				processing: false,
				autoWidth: false,
				full_row_select: false,
				scrollX: false,
				dom: "<'row'<'col-sm-12 col-md-8'l><'col-sm-12 col-md-4 p-1 bg-light rounded rounded-pill shadow-sm mb-4 search_div'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
			},
			{
				// extra_data
				// ...
			}
		);
		$("#faculty_details").on("draw.dt", function () {
			let initial_value = $("#pills-faculty .search_div input").val();
			$("#pills-faculty .search_div").html(`
				<div id="faculty_details_filter" class="dataTables_filter">
					<div class="input-group">
						<input type="search" placeholder="Global Search" aria-describedby="button-addon1" 
							class="form-control form-control-sm border-0 bg-light" id="global_search_box_faculty"
							style="box-shadow:none;outline:none" aria-controls="faculty_details">
						<div class="input-group-append">
							<button id="button-addon1" type="submit" class="btn btn-link text-primary" style="box-shadow:none;outline:none;padding:0;z-index:20"><i class="fa fa-search" style="transform:translateX(-10px)"></i></button>
						</div>
					</div>
				</div>`
			);
			$("#pills-faculty .search_div input").val(initial_value)
			if (faculty_last_searched)
				$("#pills-faculty .search_div input").focus();
			$("#pills-faculty .datatable-column-filter-row input").on("input", function () {
				faculty_last_searched = false;
			});
			$("#global_search_box_faculty").on("input", function () {
				faculty_last_searched = true;
				var table = $.fn.dataTable.Api($("#faculty_details"));
				table.search($(this).val()).draw();
			});
		});
	}
});
function user_edit_called(id) {
	console.log(id);
	$.ajax({
		type: "POST",
		data: JSON.stringify(id),
		url: "./user_edit_called/",
		success: function (data) {
			$("#update_user_form [name='first_name']").val(data["first_name"]);
			$("#update_user_form [name='last_name']").val(data["last_name"]);
			$("#update_user_form [name='email']").val(data["email"]);
		},
	});
}
