if (!String.prototype.format) {
	String.prototype.format = function() {
		var args = arguments;
		return this.replace(/{(\d+)}/g, function(match, number) { 
		return typeof args[number] != 'undefined'
			? args[number]
			: match
		;
		});
	};
};
let s = `<div class="card shadow-sm components-section mb-4" style="border-radius: 1rem" id="error_card_{0}">
	<div class="card-body" style="border-radius: 1rem;">
		<div class="accordion accordion-flush" id="error_accordion_{0}">
			<div class="accordion-item">
				<h2 class="accordion-header" id="error_accordion_heading_{0}">
					<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
						data-bs-target="#error_accordion_collapse_{0}" aria-expanded="false"
						aria-controls="error_accordion_collapse_{0}">
						<h5>{1}</h5>
					</button>
				</h2>
				<div id="error_accordion_collapse_{0}" class="accordion-collapse collapse"
					aria-labelledby="error_accordion_heading_{0}" data-bs-parent="#error_accordion_{0}">
					<div class="accordion-body">
						<div class = "error_body">
							{2}
						</div>
						<div class="table-responsive">
							{3}
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>`;
function make_accordian(index,error_heading,error_body,table){
	let obj = $('<div/>').html(s.format(index,error_heading,error_body,table)).contents();
	obj.find("thead").addClass("thead-light");
	obj.find("th").addClass("fw-bold border-1");
	return obj;
}
$(document).ready(function () {
	console.log("asd");
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

	// $.ajax({
		// type: "post",
		// success: function (data){
			// 	// document.getElementsByClassName("response")[0].textContent = JSON.stringify(data, undefined, 2);
			// }
		// });
		
		$("#main_submit").click(function(e) {	// for testinf
			$.ajax({
				url:"../csv/",
				type : 'POST',
				success : function(data) {
					if (data['error_list'].length > 0) {
						show_errors(data['error_list']);
					}
				}
			});
		})
		$(".dropzone").submit(function(e) {
			console.log(e);
			e.preventDefault();
			var formData = new FormData();
			formData.append('file', $('#csv')[0].files[0]);			
			$.ajax({
				url:"../csv/",
				type : 'POST',
				data : formData,
				processData: false,  // tell jQuery not to process the data
				contentType: false,  // tell jQuery not to set contentType
				success : function(data) {
					if (data['error_list'].length > 0) {
						show_errors(data['error_list']);
					}
				}
			});
		});
});
function show_errors(error_list){
	// make the error_body as a li 
	$("#error_main_container").html("");
	for(i in error_list){
		let obj = make_accordian(i,error_list[i].error_name,error_list[i].error_body,error_list[i].table);
		$("#error_main_container").append(obj)
	}
}