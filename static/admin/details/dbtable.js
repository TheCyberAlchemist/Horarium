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