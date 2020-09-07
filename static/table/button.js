$(document).ready(function() {

  $('.addBut').click(function(){
    console.log("HII");
    var addB = "<tr><td class ='addRow' draggable='true' droppable='true'>Buttonasdfgh</td></tr>"
    $('tbody').append(addB);
  });
  $('.addRow').sortable();
  // $('#removeRow').click(function(){
  //   $('tbody tr:last').remove();
});
