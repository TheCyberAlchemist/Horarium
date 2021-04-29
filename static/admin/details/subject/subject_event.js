all_faculty = []
let current_faculty;
class faculty{
	constructor(id = "",short = "",name = "",remaining_load=0){
		this.id = id;
		this.name = name;
		this.short = short;
		this.remaining_load = remaining_load;
	}	
}
let remaining_lect = 0
let remaining_prac = 0
function put_data(faculty_details,remaining_l,remaining_p){
	remaining_prac = remaining_p
	remaining_lect = remaining_l
	faculty_details = faculty_details.replace(/&#34;/ig,'"',);
	console.log(faculty_details);
	json = JSON.parse(faculty_details);
	for(i in json){
		obj = json[i].fields;
		temp = new faculty(obj.id,obj.short,obj.name,obj.remaining_load);
		all_faculty.push(temp);
	}
}

function update_prompts(){
	$("#max_prac").html("Max Prac "+max_prac(current_faculty));
	$("#max_lect").html("Max Lect "+max_lect(current_faculty));
}

function add_load(id,lect,prac){
	for(i in all_faculty){
		if (all_faculty[i].id == parseInt(id)){
			current_faculty = all_faculty[i];
			all_faculty[i].remaining_load += parseInt(lect) + (parseInt(prac) * 2);
		}
	}
	remaining_prac = parseInt(remaining_prac) + parseInt(prac);
	remaining_lect = parseInt(remaining_lect) + parseInt(lect);
	update_prompts();
}
function max_prac(fac){
	remaining_load = fac.remaining_load
	if ($("#lect").val()){
		remaining_load -= parseInt($("#lect").val());
		return (remaining_prac <= Math.floor(remaining_load/2))?remaining_prac:Math.floor(remaining_load/2)
	}else{
		return (remaining_prac <= Math.floor(remaining_load/2))?remaining_prac:Math.floor(remaining_load/2)
	}

}
function max_lect(fac){
	remaining_load = fac.remaining_load
	if ($("#prac").val()){
		remaining_load -= 2 *parseInt($("#prac").val());
		return (remaining_lect <= remaining_load)?remaining_lect:remaining_load
	}else{
		return (remaining_lect <= remaining_load)?remaining_lect:remaining_load
	}
}

$(document).ready (function () {
	/////////////////////// set current_faculty //////////////////////////////
	if ($("#name").val()){
		for(i in all_faculty){
			if (all_faculty[i].id == parseInt($("#name").val())){
				current_faculty = all_faculty[i];
			}
		}
	}
	$('#select_fac').change(function() {
		$('#select_fac option').each(function() {
			if($(this).is(':selected')){
				for(i in all_faculty){
					if (all_faculty[i].id == parseInt($(this).val())){
						current_faculty = all_faculty[i];
					}}}})
		$("#prac").val(null);
		$("#lect").val(null);
		update_prompts();
	});
	$('#select_fac option').each(function() {
		if($(this).is(':selected')){
			for(i in all_faculty){
				if (all_faculty[i].id == parseInt($(this).val())){
					current_faculty = all_faculty[i];
	}}}});

	///////////////////////////////////////////////////////////////////////////
	$('#lect').on("input",function() {
		console.log($(this).val());
		prac = max_prac(current_faculty);
		lect = max_lect(current_faculty);
		if((isNaN($("#lect").val())) || parseInt($("#lect").val()) > lect){
			$("#lect").val(null);
		}
		update_prompts();
	});
	$('#prac').keyup(function() {
		prac = max_prac(current_faculty)
		lect = max_lect(current_faculty)
		if((isNaN($("#prac").val())) || parseInt($("#prac").val()) > prac){
			$("#prac").val(null);
		}	
		update_prompts();
	});
});