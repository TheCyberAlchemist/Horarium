function searchFun(){
  let filter = document.getElementById('myinput').value.toUpperCase();
  let myTable = document.getElementById('db-table');
  let tr = myTable.getElementsByTagName('tr');

  for (var i = 0; i < tr.length; i++) {
    let td = tr[i].getElementsByTagName('td')[1];
    //let td2 = tr[i].getElementsByTagName('td')[2];
      if(td){
         let textvalue = td.textContent || td.innerHTML;
        // let textvalue2 = td2.textContent || td2.innerHTML;
          if (textvalue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";

          }else{
            tr[i].style.display = "none";
          }

          // if (textvalue2.toUpperCase().indexOf(filter) > -1) {
          //   tr[i].style.display = "";
          //
          // }else{
          //   tr[i].style.display = "none";
          // }
      }
  }

}
function hideIcon(self) {
  self.style.backgroundImage = 'none';
}
