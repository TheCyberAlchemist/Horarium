jQuery(function () {
	if ($("#resource").length){
		str = "#resource";
	}else{
		str = "#faculty_home_class";
	}
	$(str).prop("disabled", true).trigger("change");
	$("#shifts").change(function(){
		$(str+" option").remove().trigger("change");
		// if ($("#faculty_form_status").html() != "Update") {
			console.log("Ajax sent",$("#faculty_form [name='first_name']").val())
			$.ajax({
				type: "GET",
				url:'./get_shift_resources',
				data:{Shift_id:$(this).val()},
				success: function (data){ 
					$(str).prop("disabled", false).trigger("change")
					data = JSON.parse(data);
					let newOption = new Option("-------","", false, false);
					$(str).append(newOption).trigger('change');
					for (resource of data){
						let type = resource.is_lab?" -- Lab":" -- Classroom";
						newOption = new Option(resource.name + type, resource.id, false, false);
						$(str).append(newOption).trigger('change');
					}
					// console.log("Ajax done ",)
					// if ($("#faculty_form_status").html() == "Update"){
					// 	$("#faculty_home_class option").remove().trigger("change");
					// }
				}
			});
		// }
	})
});