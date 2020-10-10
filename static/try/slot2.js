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
    var e_m = parseInt(this.end_time.slice(-2));
    var s_h = parseInt(this.start_time.slice(0,2));
    var e_h = parseInt(this.end_time.slice(0,2));
    var s_t = (s_h * 60 + s_m);
    var e_t = (e_h * 60 + e_m);
    s_t += addend;
    e_t += addend;
    s_h = parseInt(s_t / 60);
    s_m = parseInt(s_t % 60);
    e_h = parseInt(e_t / 60);
    e_m = parseInt(e_t % 60);
    this.start_time = this.get_String(s_h)+ ":"+this.get_String(s_m);
    this.end_time = this.get_String(e_h)+ ":"+this.get_String(e_m);
    console.log(s_t,e_t);
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
  get time(){
    return "time"
  }
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

	var add_row = document.createElement('td');
	add_row.innerHTML = '<button type="button" class="add_here">ADD</button>';
	tr.appendChild(add_row);

  return tr;
}
function get_slot(){
  form = $('#aform');
  name      =  form.find("#id_name").val();
  start_time=  form.find("#start_time").val();
  end_time  =  form.find("#end_time").val();
  is_break  =  form.find("#id_is_break").prop( "checked" );
  temp = new slot(name,start_time,end_time,is_break);
  return temp;
}
$(document).ready (function () {
  slots = []
  $(document).on("click", ".add_row" , function () {   // when add row is called
    $('.Go').show();
    $('.Go_here').hide();
    $('#aform').show();
    console.log(slots);
    if(slots.length){		                              // if not first
      last_end_time = slots[slots.length-1].end_time;
      $('#aform').find("#start_time").val(last_end_time);
    }
    else{                                             // if first input
      $('#aform').find("#start_time").val("09:00");
      $('#aform').find("#end_time").val("09:05");
    }
	});
  $(document).on("click", ".Go" , function() {    // when slot form is submitted
    temp = get_slot();
    slots.push(temp);
    form.trigger('reset');
    $("#myTable").append(return_row(temp));
    $('#aform').css("display","none");
  });
  let index;
  $(document).on("click", ".add_here" , function(){
    $('.Go_here').show();
    $('.Go').hide();
    $('#aform').show();
		selected_tr = $(this).parentsUntil("tbody").last();
    name = selected_tr.find("td").first().html();
		for (i = 0 ; i < slots.length; i++){
      if (name == slots[i].name){
        index = i;
        break;
      }
    }
    $('#aform').find("#start_time").val(slots[i].end_time);
  });
  $(document).on("click", ".Go_here" , function() {    // when slot form is submitted
    temp = get_slot();
    slots.splice(index+1,0,temp);
    for (let i = index+2; i < slots.length; i++){
      slots[i].add(temp.duration());
    }
    form.trigger('reset');
    $('#myTable tr').eq(index).after(return_row(temp));
    for (i = index;i < slots.length; i ++){
      console.log($('#myTable tr').eq(i).find("#start_time"));
      $('#myTable tr').eq(i).find("td").html(slots[i].start_time);
    }
    // $("#myTable > tbody").empty();  // insert temp into the next row in place of empting the body
    // for (i in slots){
    //   $("#myTable").append(return_row(slots[i]));
    // }
    $('#aform').css("display","none");
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