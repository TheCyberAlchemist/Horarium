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
function hover(self,link) {
	console.log(link);
  	self.setAttribute("src",link);
}

function unhover(self,link){
	self.setAttribute("src",link);
}

