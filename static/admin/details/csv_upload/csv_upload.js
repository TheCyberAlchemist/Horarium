if (!String.prototype.format) {
  String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
      return typeof args[number] != "undefined" ? args[number] : match;
    });
  };
}
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
						</div>
						<div class="table-responsive">
							{2}
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>`;
let a = [] ;
function make_accordian(index,error_heading,error_body,table){
	let obj = $('<div/>').html(s.format(index,error_heading,table)).contents();
	obj.find("thead").addClass("thead-light");
	if (typeof(error_body) == "string"){	// if only one statement is in body
		obj.find(".error_body").append(`<span class="list-group-item list-group-item-action list-group-item-danger mb-3">${error_body}</span>`);
	}
	else{	// if body has multiple statements
		obj.find(".error_body").append("<ul class = 'error_ul list-group-item list-group-item-action list-group-item-danger mb-3' >")
		for (stmt of error_body){
			obj.find(".error_body").append("<li>" + stmt + "</li>");
		}
		obj.find(".error_body").append("</ul>")
	}
	a.push(error_body);
	obj.find("th").addClass("fw-bold border-1");
	return obj;
}
$(document).ready(function () {
  $("#csv_select").select2();
  
  reset_main_form();

  var csrftoken = Cookies.get("csrftoken");
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  // Ensure jQuery AJAX calls set the CSRF header to prevent security errors
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  // $.ajax({
  // type: "post",
  // success: function (data){
  // 	// document.getElementsByClassName("response")[0].textContent = JSON.stringify(data, undefined, 2);
  // }
  // });
  $("#main_form").submit(function (e) {
	e.preventDefault();
	let csv_type = $("#csv_select").val()
	let my_file = $("#csv")[0].files[0]
	if (Boolean(csv_type) && Boolean($("#csv")[0].value)){ // if csv_type is selected and file uploaded
		var formData = new FormData();
		formData.append("file",my_file);
		formData.append('csv_input',csv_type);
		$.ajax({
			url: "../csv/",
			type: "POST",
			data: formData,
			processData: false, // tell jQuery not to process the data
			contentType: false, // tell jQuery not to set contentType
			success: function (data) {
				$("#error_main_container").html("");
				console.log("here")
				reset_main_form();
				if (data["error_list"].length > 0) {
					show_errors(data["error_list"]);
				}
			},
		});
	}else{
		Swal.fire(
			'Oh! This should not happen',
			'Try uploading the file or fill the details again',
			'info'
		)
	}
  });
  $(".image-upload-wrap").bind("dragover", function () {
    $(".image-upload-wrap").addClass("image-dropping");
  });
  $(".image-upload-wrap").bind("dragleave", function () {
    $(".image-upload-wrap").removeClass("image-dropping");
  });
});
function show_errors(error_list) {
  // make the error_body as a li
  for (i in error_list) {
    let obj = make_accordian(i, error_list[i].error_name, error_list[i].error_body, error_list[i].table);
    $("#error_main_container").append(obj);
  }
}
function reset_main_form(){
	$("#main_form")[0].reset();
	$('#csv_select').trigger('change');

	// $("#csv_select").val("");
	removeUpload();
}
/* #region  CSV_Upload js  */

function readURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$(".image-upload-wrap").hide();

			$(".file-upload-image").attr("src", e.target.result);
			$(".file-upload-content").show();

			$(".image-title").html(input.files[0].name);
		};

		reader.readAsDataURL(input.files[0]);
	} else {
		removeUpload();
	}
}

function removeUpload() {
	$(".file-upload-input").replaceWith($(".file-upload-input").clone());
	$(".file-upload-content").hide();
	$(".image-upload-wrap").show();
}
  

/* #endregion */
