// nothing must be shown on the page at first but the table if present .
// now there must be a button that reads delete all 
// then first form must be then shown and rest is same

var shift_start_time;
var shift_end_time;
slots = [];
class slot{
	constructor(id = "",name = "",start_time = 0 ,end_time= 0,is_break=0){
    this.id = id;
		this.name = name;
		this.start_time = start_time;
    this.end_time = end_time;
    this.is_break = is_break;
    this.shift_id;
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
  is_valid(i){
    if (greater_than(this.start_time,this.end_time) || this.start_time == this.end_time){
      return false;
    }else if (greater_than(this.end_time,shift_end_time)){
      return false;
    }
    if (i != 0){
      if(slots[i-1].end_time != this.start_time){
        console.log(slots[i-1].end_time , this.start_time);
        return false;
      }
    }
    return true;
  }
}

function set_shift(s_t,e_t,old_data){
  shift_start_time = s_t.slice(0,5);
  shift_end_time = e_t.slice(0,5);
  console.log(e_t);
  old_data = old_data.replace(/&#34;/ig,'"',);
  json = JSON.parse(old_data);
  for(i in json){
    temp = new slot();
    obj = json[i].fields;
    temp.id = json[i].pk;
    temp.name = obj.name;
    temp.start_time = obj.start_time.slice(0, -3);
    temp.end_time = obj.end_time.slice(0, -3);
    temp.is_break = obj.is_break;
    slots.push(temp);
  }
  // var json = JSON.parse();
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
var pen_link;
function put_pen(link){
  pen_link = link;
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
  
  edit.innerHTML = '<a href=""><i class="fas fa-edit"></i></a>';
//   edit.innerHTML = '<a><i class="fas fa-edit">dd</i></a>'
  edit.className = "edit_buttons";
  tr.appendChild(edit);
  
  return tr;
}

function get_slot(){
  form = $('#slot_form');
  name      =  form.find("#id_name").val();
  start_time=  form.find("#start_time").val();
  end_time  =  form.find("#end_time").val();
  is_break  =  form.find("#id_is_break").prop( "checked" );
  temp = new slot("",name,start_time,end_time,is_break);
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
  let min = temp_slot.duration();
  console.log(temp_slot);
  $("#get_remainder").html("Remaining Time :: "+parseInt(min/60) + " hr(s)\t"+(min%60) + " min(s)" );
  return temp_slot.duration();
}

function check_name(name,edit){
  if (form.find("#id_is_break").prop( "checked" ) && ( name == get_name() || name.length == 1)){
    return false;
  }
  if(!edit){
    for (i in slots){
      if (slots[i].name == name)
        return false;
    }
  }
  return true;
}

jQuery(function () {
  for (i in slots){
    $("#myTable").append(return_row(slots[i]));
  }
  $("#remainder_th").hide();
  $("#edit").hide();
  $("#Go").hide();
  $("#Go_here").hide();
  $('#first_form').hide();
  $('#add_slot_form').hide();
  $(".submit_button").hide();
  $(".edit_buttons").hide();
  ////////////////////// When edit is clicked ///////////////////////////
  $(document).on("click",'#main_edit',function(){
    $('#first_form').show();
    $("#first_form").css({ // to make slotDetails Pop Up in center
      "position": "absolute",
      "top": "50%",
      "left": "50%",
      "transform": "translate(-50%,-50%)",
      "opacity": "1",
      "z-index": "100",
    });
    $("#whole_container_id,.submit_button_container").addClass("blur_background");
  });
  ////////////////////// When first_form is submitted ///////////////////////////
  $(document).on("click",'#first_form_submit',function(){
    nomenclature = $("[name='Naming']").val();
    duration = $("[name='Duration']").val()
    $("#whole_container_id,.submit_button_container").removeClass("blur_background"); //from #first_form in form.js
    $("#whole_container_id,.submit_button_container").css({"transition" : "0s"});

    $('#first_form').hide();
    $('#main_edit').hide();
    $(".edit_buttons").show();
    $('#add_slot_form').show();
    $("#slot_form").hide();
    $('#add_row').show();
    $(".submit_button").show();
    $("#remainder_th").show();
    get_remainder();
  });
  

  $(document).on("click", "#add_row" , function () {   // when add row is called
    $('#Go').show();
    $("#edit").hide();
    $('#slot_form').show();
    $('#add_row').hide();
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
    valid_input();
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
    if(!temp.is_valid(slots.length)){
      window.alert("Invalid time given");
      return;
    }
    slots.push(temp);
    form.trigger('reset');
    $("#myTable").append(return_row(temp));
    $('#slot_form').hide();
    $('#Go').hide();
    $('#add_row').show();

    get_remainder();
  });

  let index;

  $(document).on("click", ".add_here" , function(){
    $('#Go_here').show();
    $('#slot_form').show();
		selected_tr = $(this).parentsUntil("tbody").last();
    name_td = selected_tr.find("td").first().html();
		for (i = 0 ; i < slots.length; i++){
      if (name_td == slots[i].name){
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
    if(!temp.is_valid(index)){
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
    $("#Go").hide();
    $('#slot_form').show();
    $('#add_row').hide();
    selected_tr = $(this).parentsUntil("tbody").last();
    name_td = selected_tr.find("td").first().html();
		for (i = 0 ; i < slots.length; i++){
      if (name_td == slots[i].name){
        index = i;
        break;
      }
    }
    old_duration = slots[index].duration();
    $('#slot_form').find("#id_name").val(slots[index].name);
    $('#slot_form').find("#start_time").val(slots[index].start_time);
    $('#slot_form').find("#end_time").val(slots[index].end_time);
    $('#slot_form').find("#id_is_break").prop( "checked" ,slots[index].is_break);
    valid_input();
  });

  $(document).on("click", "#edit" , function(){
    form = $('#slot_form');
    if(!check_name(form.find("#id_name").val(),true)){
      window.alert("Invalid name given.");
      return;
    }
    temp = get_slot();
    if(!temp.is_valid(index)){
      window.alert("Invalid time given");
      return;
    }
    temp.id = slots[index].id;
    slots[index] = temp;
    new_duration = temp.duration()
    delta = new_duration-old_duration;
    for (let i = index+1; i < slots.length; i++){
      slots[i].add(delta);
      console.log(slots[i].is_valid(i));
      if (!slots[i].is_valid(i)){
        console.log(i);
        while (slots.length > i){
          console.log("l");
          slots.pop()
        }
        break;
        // slots.splice(index, 1);
      }
    }
    $("#myTable > tbody").empty();  // insert temp into the next row in place of empting the body
    for (i in slots){
      $("#myTable").append(return_row(slots[i]));
    }

    $('#slot_form').hide();
    $('#edit').hide();
    $('#add_row').show();

    get_remainder();
  });

});


function submited(){
  var data = {
    'slots':slots,
    'days': [$("[name='day1']").val(), $("[name='day2']").val()]
  };
  console.log(JSON.stringify(data));
	$.ajax({
		type: "post",
		data: JSON.stringify(data),
		success: function (){
      location.reload();
		}
	});
}