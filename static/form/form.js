$(document).ready(function () {
	checkSelected(); // if any selected for delete already
	////////////// ajax setup   /////////////////////////
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

	/* ///////////TO UpperCase/////////////// */

	$(".submit_button").click(function () {
		if ($(".short_names").length)
			$(".short_names").val($(".short_names").val().toUpperCase());
	}); /////////// Can Teach ///////////////////

	/**/ $(".can_container li :checkbox").on("click", function () {
		var $chk = $(this);
		var $li = $chk.closest("li");
		var $ul, $parent;
		if ($li.has("ul")) {
			$li.find(":checkbox").not(this).prop("checked", this.checked);
		}
		do {
			$ul = $li.parent();
			$parent = $ul.siblings(":checkbox");
			if ($chk.is(":checked")) {
				$parent.prop(
					"checked",
					$ul.has(":checkbox:not(:checked)").length == 0
				);
			} else {
				$parent.prop("checked", false);
			}
			$chk = $parent;
			$li = $chk.closest("li");
		} while ($ul.is(":not(.someclass)"));
	});

	/** //////////Subject Color Palette //////////////////*/
	$(".colors").click(function () {
		if ($(".colors").css({ border: "none" })) {
			$(this).css({ border: "5px solid black" });
		}
		// else {
		//   $(this).css({"border":"none","borderRadius" :"7px","opacity":"1" });
		// }
	});

	valid_input();
	$(".form_input").change(function () {
		valid_input();
	});
	$(".form_input").focus(function () {
		$(this).next(".form_input_label").find(".text").css({
			top: "-.7em",
			left: ".5px",
			transition: ".2s",
			"font-size": "16px",
			color: "rgb(185, 184, 184)",
		});
	});

	$(".form_input").blur(function () {
		if ($(this).prop("type") != "time") {
			if (!$(this).val()) {
				$(this).next().find(".text").css({
					position: "absolute",
					top: " 1.2em",
					left: "2em",
					color: "white",
					"pointer-events": "none",
					"user-select": "none",
					"font-size": "18px",
					transition: ".4s",
				});
			}
		}
	});
	$(".form_hider").click(function () {
		$(".myform").hide();
		$(".form_visibility_img_container").show();
		$(".pagination_container").hide();
		$("#add_row").show();
	});

    /////For Pagination of Faculty Page
    if(document.getElementsByClassName("pagination_container")[0]) {
        $('#first').click(function() {
            $(this).parent().addClass("active");
            $("#second").parent().removeClass("active");
            $("#third").parent().removeClass("active");

            $("#first_page").css("display","block");
            $("#second_page").css("display","none");
            $("#third_page").css("display","none"); 
        })

        $('#second').click(function() {
            $(this).parent().addClass("active");
            $("#first").parent().removeClass("active");
            $("#third").parent().removeClass("active");

            $("#first_page").css("display","none");
            $("#second_page").css("display","block");
            $("#third_page").css("display","none");
        })

        $('#third').click(function() {
            $(this).parent().addClass("active");
            $("#second").parent().removeClass("active");
            $("#first").parent().removeClass("active");

            $("#first_page").css("display","none");
            $("#second_page").css("display","none");
            $("#third_page").css("display","block");
        })
    }
});
function valid_input() {
	var inputs = $(".form_input");
	inputs.each(function (i, obj) {
		if ($(this).val()) {
			$(this).next().find(".text").css({
				top: "-.7em",
				left: ".5px",
				transition: ".2s",
				"font-size": "16px",
				color: "rgb(185, 184, 184)",
			});
		}
	});
	var update_div = $(".update_div");
	update_div.next().find(".text").css({
		top: "-.7em",
		left: ".5px",
		transition: ".2s",
		"font-size": "16px",
		color: "rgb(185, 184, 184)",
	});
	update_div.css({
		top: "6px",
		color: "grey",
		"user-select": "none",
	});
}
function visibility1(self) {
	var a = document.getElementById("myinput1");
	var b = document.getElementById("hide1");
	var c = document.getElementById("hide2");

	if (a.type === "password") {
		a.type = "text";
		b.style.display = "inline";
		c.style.display = "none";
	} else if (a.type === "text") {
		a.type = "password";
		b.style.display = "none";
		c.style.display = "inline";
	}
}

function visibility2() {
	var x = document.getElementById("myinput2");
	var y = document.getElementById("hide3");
	var z = document.getElementById("hide4");

	if (x.type === "password") {
		x.type = "text";
		y.style.display = "inline";
		z.style.display = "none";
	} else if (x.type === "text") {
		x.type = "password";
		y.style.display = "none";
		z.style.display = "inline";
	}
}

function delete_entries(id = false) {
	if (id){	// if faculty in user_details
		var checked = $('input[name="del1"]:checked').map(function () {return this.value;}).get();
		var inner_html = $('input[name="del1"]:checked').map(function () {return this.attributes.input_name.value;}).get().toString().split(',');
	}else{
		var checked = $('input[name="del"]:checked').map(function () {return this.value;}).get();
		var inner_html = $('input[name="del"]:checked').map(function () {return this.attributes.input_name.value;}).get().toString().split(',');
	}
	console.log(checked);
	let delete_message = "";
	for (i in inner_html){
		delete_message += "<li>" + inner_html[i] + "</li>";
	}
	let state = JSON.stringify(checked);
	
	if (checked.length) {
		// checkes if one or more are selected or not
		// console.log(state)
		const swalWithBootstrapButtons = Swal.mixin({
			customClass: {
			  confirmButton: 'btn btn-success',
			  cancelButton: 'btn btn-danger'
			},
			buttonsStyling: false
		  })
		  swalWithBootstrapButtons.fire({
			title: `Are you sure?`,
			html:`You won't be able to revert this!<br><ul>`+delete_message+`</ul>`,
			icon: 'warning',
			showCancelButton: true,
			confirmButtonText: 'No, cancel!',
			cancelButtonText: 'Yes, delete it! ',
			reverseButtons: true
		  }).then((result) => {
			if (result.isConfirmed) {
				swalWithBootstrapButtons.fire(
					'Cancelled',
					'Your imaginary file is safe :)',
					'error'
					)
				} else if (result.dismiss === Swal.DismissReason.cancel) {
					swalWithBootstrapButtons.fire({
						title:'Deleted!',
						text:'Your file has been deleted.',
						icon:'success',
						showConfirmButton: false,
					})
					$.ajax({
						type: "post",
						data: state,
						success: function () {
							// reload page after success of post
							setTimeout(() => {  location.reload(); }, 1000);
						},
					});
				}
		  })


		// swal({
		// 	title: "Warning!",
		// 	text:
        // "This Data will be deleted :: \n ->" + delete_message,
		// 	icon: "warning",
		// 	dangerMode: true,
		// 	buttons: ["Cancel", "Delete"],
		// }).then((willDelete) => {
		// 	if (willDelete) {
		// 		swal("", {
		// 			icon: "success",
		// 			text: "Deleted Successfully!",
		// 		});
				// $.ajax({
				// 	type: "post",
				// 	data: state,
				// 	success: function () {
				// 		location.reload(); // reload page after success of post
				// 	},
				// });
		// 	} else {
		// 		swal("Your changes are not saved!");
		// 	}
		// });
	}
}

function form_visibility(update = false) {
	var form = document.getElementsByClassName("myform")[0];
	var p = document.getElementById("myp");
	var pages = document.getElementsByClassName("pagination_container")[0];
	var container = document.getElementsByClassName("form_visibility_img_container")[0];
	if (update) {
		container.style.display = "none";
		return;
	}
	if (form.style.display == "none") {
		// p.innerHTML = "Close Form";
		container.style.display = "none";
		form.style.display = "block";
		if (pages) pages.style.display = "";
	} else {
		p.innerHTML = "Show Form";
		form.style.display = "none";
		if (pages) pages.style.display = "none";
	}
}

function show_error(json_error) {
	// console.log(json_error);
	json = JSON.parse(json_error.replace(/&#34;/gi, '"'));
	for (i in json) {
		var input = $("[name=" + i + "]");
		console.log(input);
		// change css here
		$(".myform .input_container :input").val("");
	}

	form_visibility();
	for (i in json) {
		input = $("[name=" + i + "]");
		break;
	}
	input.focus();
	// input[0].setCustomValidity('hii');
}
