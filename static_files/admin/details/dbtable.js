$(document).ready(function () {
	checkSelected(); // if any selected for delete already
});
function searchFun(){
	let filter = document.getElementById('myinput').value.toUpperCase();
	let myTable = document.getElementById('db_table');
	let tr = myTable.getElementsByTagName('tr');
	for (var i = 1; i < tr.length; i++) {
		let td = tr[i].getElementsByTagName('td');
		let matched = false;
		for (var j = td.length - 2; j >= 0; j--) {
			if(td[j]){
				let textvalue = td[j].textContent || td[j].innerHTML;
				if (textvalue.toUpperCase().indexOf(filter) > -1) {
					matched = true;
					tr[i].style.display = "";
		    	}
			}
		}
		if (!matched){
			tr[i].style.display = "none";
		}
	}
}

function checkAll(id = false){
	// if faculty in user_details then id = del1
	if (id){
		var parent = document.getElementById('parent1');
		var input = document.getElementsByClassName('del1_input');
	}else{
		var parent = document.getElementById('parent');
		var input = document.getElementsByClassName('del_input');
	}
	if(parent.checked == true){	
	  for(var i=0; i<input.length;i++){
		  if(input[i].checked == false ) {
			input[i].checked = true; 
		  }
	  }  
	}
	if(parent.checked == false){
	  for(var i=0; i<input.length;i++){
		  if(input[i].checked ==true){
			input[i].checked = false; 
		  }
	  }
	}
	if (id){
		checkSelected(id);
	}else{
		checkSelected();
	}
}

function checkSelected(id = "del"){
	// if faculty in user_details then id = del1
	var child = document.getElementsByName(id);
	var del = document.getElementById(id);
	var check = false;
	for(var c in child){
		if(child[c].checked == true){
			del.style.display = "inline";
			check = true;
			break;
		}
	}
	if(!check){
		del.style.display = "none";
	}
}

function delete_entries(id = false,reload = true) {
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
					'Your data is safe :)',
					'error'
					)
				} else if (result.dismiss === Swal.DismissReason.cancel) {
					swalWithBootstrapButtons.fire({
						title:'Deleted!',
						text:'Your data has been deleted.',
						icon:'success',
						showConfirmButton: false,
					})
					$.ajax({
						type: "post",
						data: state,
						success: function () {
							// reload page after success of post
							if (reload)
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