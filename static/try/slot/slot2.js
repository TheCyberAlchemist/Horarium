var shift_start_time;
var shift_end_time;
function set_shift(s_t,e_t){
  shift_start_time = s_t;
  shift_end_time = e_t;
  console.log(shift_end_time,shift_start_time);
}
class slot{
	constructor(name = "",start_time = 0 ,end_time= 0,is_break=0){
		this.name = name;
		this.start_time = start_time;
    this.end_time = end_time;
		this.is_break = is_break;
	}
	duration(){
    var s_m = parseInt(this.start_time.slice(-2));
    var e_m = parseInt(this.end_time.slice(-2));
    var s_h = parseInt(this.start_time.slice(0,2));
    var e_h = parseInt(this.end_time.slice(0,2));
		return (e_h * 60 + e_m)-(s_h * 60 + s_m);
  }
  get_String(num){
    var temp = num < 10 ? "0" + String(num): String(num);
    return(temp)
  }
	add(addend){
    var s_m = parseInt(this.start_time.slice(-2));
    var s_h = parseInt(this.start_time.slice(0,2));
    var s_t = (s_h * 60 + s_m);
    var e_m = parseInt(this.end_time.slice(-2));
    var e_h = parseInt(this.end_time.slice(0,2));
    var e_t = (e_h * 60 + e_m);
    s_t += addend;
    e_t += addend;
    s_h = parseInt(s_t / 60);
    s_m = parseInt(s_t % 60);
    e_h = parseInt(e_t / 60);
    e_m = parseInt(e_t % 60);
    this.start_time = this.get_String(s_h)+ ":"+this.get_String(s_m);
    this.end_time = this.get_String(e_h)+ ":"+this.get_String(e_m);
	}
	subtract(subtraend){
    var s_m = parseInt(this.start_time.slice(-2));
    var e_m = parseInt(this.end_time.slice(-2));
    var s_h = parseInt(this.start_time.slice(0,2));
    var e_h = parseInt(this.end_time.slice(0,2));
    var s_t = (s_h * 60 + s_m);
    var e_t = (e_h * 60 + e_m);
    s_t -= subtraend;
    e_t -= subtraend;
    s_h = parseInt(s_t / 60);
    s_m = parseInt(s_t % 60);
    e_h = parseInt(e_t / 60);
    e_m = parseInt(e_t % 60);
    this.start_time = this.get_String(s_h)+ ":"+this.get_String(s_m);
    this.end_time = this.get_String(e_h)+ ":"+this.get_String(e_m);
  }
  get_end(duration){
    var s_m = parseInt(this.start_time.slice(-2));
    var s_h = parseInt(this.start_time.slice(0,2));    
    var s_t = (s_h * 60 + s_m);
    var e_t = s_t + parseInt(duration);
    var e_h = parseInt(e_t / 60);
    var e_m = parseInt(e_t % 60);
    this.end_time = this.get_String(e_h)+ ":"+this.get_String(e_m);
    return this.end_time;
  }
  get_start(){
    var s_m = parseInt(this.start_time.slice(-2));
    var s_h = parseInt(this.start_time.slice(0,2));
    this.start_time = this.get_String(s_h)+ ":"+this.get_String(s_m);
    return this.start_time;
  }
  is_valid(){
    if (greater_than(this.start_time,this.end_time) || this.start_time == this.end_time){
      return false;
    }
    else if (greater_than(this.end_time,shift_end_time)){
      return false;
    }
    return true;
  }
}

function greater_than(a,b){
  var a_m = parseInt(a.slice(-2));
  var a_h = parseInt(a.slice(0,2));
  var a_t = (a_h * 60 + a_m);
  var b_m = parseInt(b.slice(-2));
  var b_h = parseInt(b.slice(0,2));
  var b_t = (b_h * 60 + b_m);
  if (a_t > b_t)
    return 1;
  return 0;
}

function return_row(slot){
  var tr = document.createElement('tr');

  var name = document.createElement('td');
  name.innerHTML = slot.name;
  tr.appendChild(name);
  
  var start_time= document.createElement('td');
	start_time.innerHTML = slot.start_time;
	tr.appendChild(start_time);

	var end_time= document.createElement('td');
	end_time.innerHTML = slot.end_time;
	tr.appendChild(end_time);
	
	var is_break = document.createElement('td');
	is_break.innerHTML = slot.is_break ? "True":"False";
	tr.appendChild(is_break);

  var edit = document.createElement('td');
	edit.innerHTML = '<button type="button" class="edit">Edit</button>';
  tr.appendChild(edit);
  
	var add_row = document.createElement('td');
	add_row.innerHTML = '<button type="button" class="add_here">ADD</button>';
	tr.appendChild(add_row);

  return tr;
}

function get_slot(){
  form = $('#slot_form');
  name      =  form.find("#id_name").val();
  start_time=  form.find("#start_time").val();
  end_time  =  form.find("#end_time").val();
  is_break  =  form.find("#id_is_break").prop( "checked" );
  temp = new slot(name,start_time,end_time,is_break);
  return temp;
}

function get_name(i){
  if (!i){
    i = 0;
    for (var j in slots){
      if (!slots[j].is_break){
        i++;
      }
    }
  }
  if (nomenclature == "numbers"){
    return (parseInt(i)+1).toString();
  }else if(nomenclature == "small"){
    return String.fromCharCode('a'.charCodeAt() + parseInt(i));
  }else if(nomenclature == "capital"){
    return String.fromCharCode('A'.charCodeAt() + parseInt(i));
  }
}

function get_remainder(){
  temp_slot = new slot();
  temp_slot.start_time = slots[slots.length-1].end_time;
  temp_slot.end_time = shift_end_time;
  console.log(temp_slot.duration());
  return temp_slot.duration();
}

function check_name(name,edit){
  if (form.find("#id_is_break").prop( "checked" ) && ( name == get_name() || name.length == 1)){
    return false;
  }
  if(!edit){
    console.log(edit);
    for (i in slots){
      if (slots[i].name == name)
        return false;
    }
  }
  return true;
}

$(document).ready (function () {
  slots = []
  $("#edit").hide();
  $("#Go").hide();
  $("#Go_here").hide();
  $('#first_form').show();

  $(document).on("click",'#first_form_submit',function(){
    nomenclature = $("input[name='Naming']:checked").val();
    duration = $("#Duration").val()
    var index = 0;
    $('#first_form').hide();
    // temp_slot = new slot();
    // temp_slot.start_time = shift_start_time;
    // console.log(temp_slot.get_end(duration));
    // slots.push(temp_slot);
    // while (true){
    //   temp_slot = new slot();
    //   temp_slot.start_time = slots[index].end_time;
    //   temp_slot.get_end(duration);
    //   if (greater_than(temp_slot.end_time,shift_end_time))
    //     break;
    //   slots.push(temp_slot);
    //   index += 1 ;
    // }
    // console.log(slots);
    // for (i in slots){
    //   if (nomenclature == "numbers"){
    //     slots[i].name = (parseInt(i)+1).toString();
    //   }else if(nomenclature == "small"){
    //     slots[i].name = String.fromCharCode('a'.charCodeAt() + parseInt(i));
    //   }else if(nomenclature == "capital"){
    //     slots[i].name = String.fromCharCode('A'.charCodeAt() + parseInt(i));
    //   }
    //   $("#myTable").append(return_row(slots[i]));
    // }
    $("#myTable").show();
  });

  $('#slot_form').hide();

  $(document).on("click", "#add_row" , function () {   // when add row is called
    name = 1;
    $('#Go').show();
    $('#slot_form').show();
    if(slots.length){		                              // if not first
      last_end_time = slots[slots.length-1].end_time;
      temp_slot = new slot();
      temp_slot.start_time = last_end_time;
      $('#slot_form').find("#id_name").val(get_name());
      $('#slot_form').find("#start_time").val(last_end_time);
      $('#slot_form').find("#end_time").val(temp_slot.get_end(duration));
    }
    else{                                             // if first input
      $('#slot_form').find("#start_time").val();
      temp_slot = new slot();
      temp_slot.start_time = shift_start_time;
      $('#slot_form').find("#start_time").val(temp_slot.get_start());
      $('#slot_form').find("#end_time").val(temp_slot.get_end(duration));
      $('#slot_form').find("#id_name").val(get_name())
      $('#slot_form').find("#is_break").hide();
      $('#slot_form').find("#id_is_break").prop( "checked" ,false);
    }
	});
  
  $(document).on("click", "#Go" , function() {    // when slot form is submitted
    $('#slot_form').find("#is_break").show();
    form = $('#slot_form');
    console.log(form.find("#id_name").val().length);
    if(!check_name(form.find("#id_name").val())){
      window.alert("Invalid name given.");
      return;
    }
    temp = get_slot();
    if(!temp.is_valid()){
      window.alert("Invalid time given");
      return;
    }
    slots.push(temp);
    form.trigger('reset');
    $("#myTable").append(return_row(temp));
    $("#myTable").show();
    $('#slot_form').hide();
    $('#Go').hide();
    get_remainder();
  });

  let index;

  $(document).on("click", ".add_here" , function(){
    $('#Go_here').show();
    $('#slot_form').show();
		selected_tr = $(this).parentsUntil("tbody").last();
    name = selected_tr.find("td").first().html();
		for (i = 0 ; i < slots.length; i++){
      if (name == slots[i].name){
        index = i;
        break;
      }
    }
    temp_slot = new slot();
    temp_slot.start_time = slots[index].end_time;
    var num = 0;
    for (i in slots){
      if (i>index)
        break;
      if (!slots[i].is_break)
      num++;
    }
    $('#slot_form').find("#id_name").val(get_name(num));
    $('#slot_form').find("#start_time").val(temp_slot.start_time);
    $('#slot_form').find("#end_time").val(temp_slot.get_end(duration));
  });
  
  $(document).on("click", "#Go_here" , function() {    // when slot form is submitted
    form = $('#slot_form');
    if(!check_name(form.find("#id_name").val())){
      window.alert("Invalid name given.");
      return;
    }
    temp = get_slot();
    if(!temp.is_valid()){
      window.alert("Invalid time given");
      return;
    }
    slots.splice(index+1,0,temp);
    for (let i = index+2; i < slots.length; i++){
      slots[i].add(temp.duration());
    }
    $("#myTable > tbody").empty();  // insert temp into the next row in place of empting the body
    for (i in slots){
      $("#myTable").append(return_row(slots[i]));
    }
    $('#Go_here').hide();
    $('#slot_form').hide();
    get_remainder();
  });
  
  $(document).on("click", ".edit" , function(){
    $("#edit").show();
    $('#slot_form').show();
    selected_tr = $(this).parentsUntil("tbody").last();
    name = selected_tr.find("td").first().html();
		for (i = 0 ; i < slots.length; i++){
      if (name == slots[i].name){
        index = i;
        break;
      }
    }
    old_duration = slots[index].duration();
    $('#slot_form').find("#id_name").val(slots[index].name);
    $('#slot_form').find("#start_time").val(slots[index].start_time);
    $('#slot_form').find("#end_time").val(slots[index].end_time);
    $('#slot_form').find("#id_is_break").prop( "checked" ,slots[index].is_break);
  });

  $(document).on("click", "#edit" , function(){
    form = $('#slot_form');
    if(!check_name(form.find("#id_name").val(),true)){
      window.alert("Invalid name given.");
      return;
    }
    temp = get_slot();
    if(!temp.is_valid()){
      window.alert("Invalid time given");
      return;
    }
    slots[index] = temp;
    new_duration = temp.duration()
    delta = new_duration-old_duration;
    for (let i = index+1; i < slots.length; i++){
      slots[i].add(delta);
    }
    $("#myTable > tbody").empty();  // insert temp into the next row in place of empting the body
    for (i in slots){
      $("#myTable").append(return_row(slots[i]));
    }
    $('#slot_form').hide();
    $("#edit").hide();
    get_remainder();
  });

});


function submited(){
	$.ajax({
		type: "post",
		data: JSON.stringify(slots),
		success: function (){
		}
	});
}